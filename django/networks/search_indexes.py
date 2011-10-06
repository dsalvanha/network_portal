import datetime
from haystack.indexes import *
from haystack import site
from networks.models import Gene

class GeneIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    species = CharField(model_attr='species__name')
    species_short_name = CharField(model_attr='species__short_name')
    chromosome = CharField(model_attr='chromosome__name')
    chromosome_length = IntegerField(model_attr='chromosome__length')
    chromosome_topology = CharField(model_attr='chromosome__topology')
    name = CharField(model_attr='name')
    common_name = CharField(model_attr='common_name')
    type = CharField(model_attr='type')
    strand = CharField(model_attr='strand')
    description = CharField(model_attr='description')
    network_name = CharField(model_attr='network__name')
    network_description = CharField(model_attr='network__description')
    network_created_at = DateTimeField(model_attr='network__created_at')
    condition_name = CharField(model_attr='condition__name')
    influence_name = CharField(model_attr='influence__name')
    influence_type = CharField(model_attr='influence__type')
    bicluster_k = IntegerField(model_attr='bicluster__k')
    bicluster_residual = IntegerField(model_attr='bicluster__residual')
    motif_position = IntegerField(model_attr='motif__position')
    motif_sites = IntegerField(model_attr='motif__sites')
    motif_e_value = IntegerField(model_attr='motif__e_value')    
    annotation_target_type = CharField(model_attr='annotation__target_type')
    annotation_title = CharField(model_attr='annotation__title')
    annotation_description = CharField(model_attr='annotation__description')
    annotation_source = CharField(model_attr='annotation__source')

    def index_query(self):
        """Used when the entire index for model is updated."""
        return Gene.objects.filter(network_created_at__lte=datetime.datetime.now())

site.register(Gene, GeneIndex)
