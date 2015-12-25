from ladder.models import Player, Match
from django.forms import ModelForm, DateTimeInput
from django.core.exceptions import ValidationError

class MatchForm(ModelForm):
    class Meta:
        model = Match
        fields = ['black',
                  'white',
                  'date',
                  'komi',
                  'handicap',
                  'result',
                  'result_type',
                  'score_black',
                  'score_white']

        widgets = {
            'date': DateTimeInput(attrs={
                'class': 'datepicker'
            }),
        }

    
    def clean(self):
        try:
            white = self.cleaned_data['white']
            black = self.cleaned_data['black']

            if white == black:
                raise ValidationError("White can't play herself")

            if self.cleaned_data['result'] == Match.Result.DRAW:
                # just fix it, don't raise an error
                self.cleaned_data['result_type'] = Match.ResultType.NO_RESULT
                self.cleaned_data['score_white'] = 0
                self.cleaned_data['score_black'] = 0

                white.drew_with(black)
                black.drew_with(white)
            else:
                if self.cleaned_data['result_type'] \
                                        == Match.ResultType.TERRITORY and \
                    (self.cleaned_data['score_black'] == None or \
                     self.cleaned_data['score_white'] == None):
                    raise ValidationError("Please supply scores")
                
                if self.cleaned_data['result'] == Match.Result.BLACK_WIN:
                    white.lost_to(black)
                    black.beat(white)
                else:
                    white.beat(black)
                    black.lost_to(white)

            black.save()
            white.save()
        except KeyError:
            # mandatory fields will already have been handled
            return

        return super(MatchForm, self).clean()
