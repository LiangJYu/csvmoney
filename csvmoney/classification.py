from ruamel.yaml import YAML

class classification():
    def __init__(self, path_categories='categories.yaml'):
        yaml = YAML(typ='safe')
        with open(path_categories, 'r') as fin:
            categories = yaml.load(fin)

        self.cats = []
        self.kw2cat = {}
        for key, val in categories.items():
            if val is None:
                self.cats.append(key)
                continue
            for val_key, val_val in val.items():
                self.cats.append(f'{key}/{val_key}')
                if val_val is None:
                    continue
                for val_val_val in val_val:
                    self.kw2cat[val_val_val] = f'{key}/{val_key}'

    def identify(self, description):
        '''
        Try to match keywords to description and return category
        '''
        for k, v in self.kw2cat.items():
            if k.lower() in description.lower():
                return v
        return 'uncategorized'
