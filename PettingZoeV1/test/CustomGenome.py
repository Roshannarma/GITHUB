import neat
from neat.activations import ActivationFunctionSet
from neat.attributes import FloatAttribute, BoolAttribute, StringAttribute
from neat.config import ConfigParameter, write_pretty_params
from neat.genes import BaseGene
class GenomeNodeGene(BaseGene):
    __gene_attributes__ = []

    def distance(self, other, config):
        return 0.0


class GenomeConnectionGene(BaseGene):
    __gene_attributes__ = [StringAttribute('component'),
                           FloatAttribute('value'),
                           BoolAttribute('enabled')]

    def distance(self, other, config):
        d = abs(self.value - other.value)
        return d
        # if self.component != other.component:
            # d += 1.0
        # if self.enabled != other.enabled:
            # d += 1.0
        # return d * config.compatibility_weight_coefficient


class CustomGenomeConfig(BaseGene):
    def __init__(self, params):
        # Create full set of available activation functions.
        self.activation_defs = ActivationFunctionSet()
        self.activation_options = params.get('activation_options', 'sigmoid').strip().split()
        self.aggregation_options = params.get('aggregation_options', 'sum').strip().split()

        # Gather configuration data from the gene classes.
        self.__params += CircuitNodeGene.get_config_params()
        self.__params += CircuitConnectionGene.get_config_params()

        # Use the configuration data to interpret the supplied parameters.
        for p in self.__params:
            setattr(self, p.name, p.interpret(params))

        # By convention, input pins have negative keys, and the output
        # pins have keys 0,1,...
        self.input_keys = [-i - 1 for i in range(self.num_inputs)]
        self.output_keys = [i for i in range(self.num_outputs)]

    def save(self, f):
        write_pretty_params(f, self, self.__params)


class CustomGenome(neat.DefaultGenome):
    @classmethod
    def parse_config(cls, param_dict):
        return CircuitGenomeConfig(param_dict)

    @classmethod
    def write_config(cls, f, config):
        config.save(f)

    __params = [ConfigParameter('num_inputs', int),
            ConfigParameter('num_outputs', int),
            ConfigParameter('compatibility_disjoint_coefficient', float),
            ConfigParameter('compatibility_weight_coefficient', float),
            ConfigParameter('conn_add_prob', float),
            ConfigParameter('conn_delete_prob', float),
            ConfigParameter('node_add_prob', float),
            ConfigParameter('node_delete_prob', float)]


    def __init__(self,key):
        return super().__init__(self,key)
        # pass



    # def configure_new(self,config):
        # pass



    # def configure_crossover(self,genome1,genome2,config):
        # pass



    # def mutate(self,config):
        # pass


    # def distance(self,other,config):
        # pass

    def size(self):
        return 1
