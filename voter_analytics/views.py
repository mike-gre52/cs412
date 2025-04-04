from django.shortcuts import render

# Create your views here.
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from datetime import datetime
from django.db.models import Count
from . models import Voter

import plotly
import plotly.graph_objs as go

# Create your views here.

class VotersListView(ListView):
    '''View to display list of voters'''

    template_name = "voter_analytics/voters.html"
    model = Voter
    context_object_name = "voters"
    paginate_by = 100

    def get_context_data(self, **kwargs) :
        ''' Provide context variables for use in template '''
        # start with superclass context
        context = super().get_context_data(**kwargs)
        context['years'] = list(reversed(range(1900, 2025)))
        return context


    def get_queryset(self):
        #Filter the voter query

        #all voters
        voters = super().get_queryset()
   
        #filter party
        if 'party' in self.request.GET:
            party = self.request.GET['party']
            if party != "Any":
                voters = voters.filter(party=party)

        #filter min_dob
        if 'min_dob' in self.request.GET:
            min_dob = self.request.GET['min_dob']
            if min_dob != "Any":
                min_dob = min_dob + '-01-01'
                min_dob_date = datetime.strptime(min_dob, '%Y-%m-%d').date()
                
                voters = voters.filter(date_of_birth__gt=min_dob_date)
        
        #filter max_dob
        if 'max_dob' in self.request.GET:
            max_dob = self.request.GET['max_dob']
            if max_dob != "Any":
                max_dob = max_dob + '-01-01'
                max_dob_date = datetime.strptime(max_dob, '%Y-%m-%d').date()
                
                voters = voters.filter(date_of_birth__lt=max_dob_date)

        #filter voter_score
        if 'voter_score' in self.request.GET:
            voter_score = self.request.GET['voter_score']
            if voter_score != "Any":
                voters = voters.filter(voter_score=voter_score)
        
        #filter vote years
        if 'v20state' in self.request.GET:
            v20state = self.request.GET['v20state']
            if v20state:
                voters = voters.filter(v20state=True)

        if 'v21town' in self.request.GET:
            v21town = self.request.GET['v21town']
            if v21town:
                voters = voters.filter(v21town=True)

        if 'v21primary' in self.request.GET:
            v21primary = self.request.GET['v21primary']
            if v21primary:
                voters = voters.filter(v21primary=True)

        if 'v22general' in self.request.GET:
            v22general = self.request.GET['v22general']
            if v22general:
                voters = voters.filter(v22general=True)

        if 'v23town' in self.request.GET:
            v23town = self.request.GET['v23town']
            if v23town:
                voters = voters.filter(v23town=True)
                
        return voters


class VoterDetailView(DetailView):
    '''View to show detail page for one result.'''

    template_name = 'voter_analytics/voter_detail.html'
    model = Voter
    context_object_name = 'voter'

    def get_context_data(self, **kwargs) :
        ''' Provide context variables for use in template '''
        # start with superclass context
        context = super().get_context_data(**kwargs)
        voter = context['voter']
        return context
    
class GraphsListView(ListView):
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'

    def get_context_data(self, **kwargs):
        '''
        Provide context variables for use in template
        '''
        context = super().get_context_data(**kwargs)

        party = self.request.GET.get('party', 'Any')
        min_dob = self.request.GET.get('min_dob', 'Any')
        max_dob = self.request.GET.get('max_dob', 'Any')
        voter_score = self.request.GET.get('voter_score', 'Any')
        v20state = 'v20state' in self.request.GET
        v21town = 'v21town' in self.request.GET
        v21primary = 'v21primary' in self.request.GET
        v22general = 'v22general' in self.request.GET
        v23town = 'v23town' in self.request.GET
        
        voters = Voter.objects.all()

        if party != 'Any':
            voters = voters.filter(party=party)
        if min_dob != 'Any':
            voters = voters.filter(date_of_birth__year__gte=min_dob)
        if max_dob != 'Any':
            voters = voters.filter(date_of_birth__year__lte=max_dob)
        if voter_score != 'Any':
            voters = voters.filter(voter_score=voter_score)
        if v20state:
            voters = voters.filter(v20state=True)
        if v21town:
            voters = voters.filter(v21town=True)
        if v21primary:
            voters = voters.filter(v21primary=True)
        if v22general:
            voters = voters.filter(v22general=True)
        if v23town:
            voters = voters.filter(v23town=True)

        year_data = voters.values('date_of_birth__year').annotate(count=Count('date_of_birth__year'))
        birth_years = [v['date_of_birth__year'] for v in year_data]
        birth_counts = [v['count'] for v in year_data]

        birth_graph = go.Histogram(x=birth_years, y=birth_counts, histfunc='sum', nbinsx=125)
        birth_title_text = "Distribution of Voters by Year of Birth"
        graph_birth = plotly.offline.plot({
            "data": [birth_graph],
            "layout_title_text": birth_title_text
        }, auto_open=False, output_type="div")

        context['graph_div_birth'] = graph_birth
        

        party_data = voters.values('party').annotate(count=Count('party'))
        party_labels = [v['party'] for v in party_data]
        party_values = [v['count'] for v in party_data]

        party_graph = go.Pie(labels=party_labels, values=party_values)
        party_title_text = "Voter Distribution by Party Affiliation"
        graph_party = plotly.offline.plot({
            "data": [party_graph],
            "layout_title_text": party_title_text
        }, auto_open=False, output_type="div")
        
        context['graph_div_party'] = graph_party
        election_participation = {
        'v20state': voters.filter(v20state=True).distinct().count(),
        'v21town': voters.filter(v21town=True).distinct().count(),
        'v21primary': voters.filter(v21primary=True).distinct().count(),
        'v22general': voters.filter(v22general=True).distinct().count(),
        'v23town': voters.filter(v23town=True).distinct().count(),
        }

        election_graph = go.Bar(x=list(election_participation.keys()), y=list(election_participation.values()))
        election_title_text = "Voter Participation in Elections"
        graph_election = plotly.offline.plot({
            "data": [election_graph],
            "layout_title_text": election_title_text
        }, auto_open=False, output_type="div")
        context['graph_div_election'] = graph_election
        context['voters'] = voters

        context['years'] = list(reversed(range(1900, 2025)))
        return context
        