import django
from django.db import models
from django.db import IntegrityError


def get_default_stage_state():
    """ get a default value for confirmation status; create new state if not available """
    return StageState.objects.get_or_create(name='pending')[0].id


def get_default_stage_result():
    """ get a default value for confirmation result; create new result if not available """
    return StageResult.objects.get_or_create(name='unknown')[0].id


class ReferenceTable(models.Model):
    """ abstract model for enum-based 'lookup' tables """
    name = models.CharField(max_length=64, blank=True, null=True, help_text='human readable representation of value')
    description = models.CharField(max_length=255, blank=True, null=True, help_text='description of this entry')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return self.name


class StageState(ReferenceTable):
    """
    Values to reflect the operational activity of a stage.

    default states:
        - pending   = activity on this stage is expected but has not yet started
        - started   = activity on this stage has started
        - completed = activity on this stage has completed
        - blocked   = activity on this stage is blocked by a previous stage
    """


class StageResult(ReferenceTable):
    """
    Values to reflect the outcome of a stage.

    default results:
        - success = stage completed successfully with no issues
        - fail    = stage completed with a well-defined failure condition
        - error   = stage encountered an error and could not complete
        - unknown = stage has not completed, or completion can not be determined
    """


class Sequence(models.Model):
    """ individual instance of a model_sequence entry """
    is_complete = models.BooleanField(default=False, help_text='set to true when all stages have a state of completed')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def advance(self):
        """ complete the current stage with a result of success; if not the last stage, start the next stage """
        current_stage = self.get_current_stage()
        if current_stage:
            current_stage.succeed_stage()
        try:
            next_stage = Stage.objects.get(id=current_stage.order + 1)
            next_stage.start_stage()
        except IntegrityError:
            return None

    def get_stages(self) -> models.query.QuerySet:
        """ get all the stages of this model_sequence """
        return self.stage_set.all()

    def get_completion_percentage(self) -> float:
        """ get the current completion, as a percentage, of this model_sequence """
        return self.stage_set.filter(state__name='completed').count() / self.stage_set.count()

    def get_current_stage(self):
        """ get the current stage of this model_sequence """
        remaining_stages = self.get_remaining_stages()
        if remaining_stages:
            return remaining_stages.first()

    def get_completed_stages(self) -> models.query.QuerySet:
        """ get completed stages of this model_sequence """
        return self.stage_set.filter(state__name='completed')

    def get_remaining_stages(self) -> models.query.QuerySet:
        """ get remaining (non-completed) stages of this model_sequence """
        return self.stage_set.exclude(state__name='completed')

    def add_stage(self, name: str, description: str = None, blocking: bool = None):
        """ add a stage to this model_sequence
        Parameters:
            name        - (str) name of this stage
            description - (str) description of this stage
            blocking    - (bool) set this stage to blocking
        """
        data = dict(sequence=self, name=name)
        if description:
            data['description'] = description
        if blocking:
            data['blocking'] = blocking
        Stage.objects.create(**data)

    def add_stages(self, stage_list: list):
        """ add all the stages passed as a list of dictionaries such as:
            [
                {'name': 'my_stage', 'description': 'description of my stage', },
                ...
            ]
        Parameters:
            stage_list - (list) list of dictionaries
        """
        for stage in stage_list:
            stage['sequence'] = self
            Stage.objects.create(**stage)

    @property
    def stages(self):
        return self.get_stages()


class Stage(models.Model):
    """ individual stage(s) for a model_sequence item; identifies where in the overall model_sequence a thing is; 
    includes a state and a result """
    sequence = models.ForeignKey(Sequence, on_delete=models.CASCADE, help_text='model_sequence this stage belongs to')
    name = models.CharField(max_length=64, unique=True, help_text='short reference for stage')
    description = models.CharField(max_length=255, blank=True, null=True, help_text='detailed description of stage')
    order = models.IntegerField(help_text='operational order of stage (where 1 is the first)')
    state = models.ForeignKey(StageState, default=get_default_stage_state, on_delete=models.CASCADE,
                              help_text='current activity of model_sequence stage')
    result = models.ForeignKey(StageResult, default=get_default_stage_result, on_delete=models.CASCADE,
                               help_text='outcome of model_sequence stage')
    details = models.CharField(max_length=255, blank=True, null=True,
                               help_text='additional details, such as incomplete reason')
    blocking = models.BooleanField(default=True,
                                   help_text='if True, do not continue to next stage if a failure or error occurs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

    def get_duration(self):
        """ """
        return self.updated_at - self.created_at

    def update_sequence(self):
        """ when this stage is updated (state or result) update the parent LifeCycle accordingly """
        pass

    def start_stage(self):
        """ set state of stage to 'started' """
        self.state = StageState.objects.get_or_create(name='started')[0]
        self.save()

    def fail_stage(self):
        """ set state of stage to 'started' and result to 'fail' """
        self.state = StageState.objects.get_or_create(name='completed')[0]
        self.result = StageResult.objects.get_or_create(name='fail')[0]
        self.save()

    def error_stage(self):
        """ set result of stage to 'error' """
        self.result = StageResult.objects.get_or_create(name='error')[0]
        self.save()

    def succeed_stage(self):
        """ set state of stage to 'started' and result to 'success' """
        self.state = StageState.objects.get_or_create(name='completed')[0]
        self.result = StageResult.objects.get_or_create(name='success')[0]
        self.save()

    def save(self, *args, **kwargs):
        if not self.pk and not self.order:
            stage_count = self.sequence.stage_set.count()
            self.order = stage_count + 1
        else:
            if self == self.sequence.stage_set.last():
                if self.sequence.stage_set.filter(state__name='completed').count() == self.sequence.stage_set.count():
                    self.sequence.is_complete = True
                    self.sequence.save()
        super(Stage, self).save(*args, **kwargs)

    duration = property(get_duration)
