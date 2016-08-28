# coding=utf-8
import argparse
import plistlib
from kolor import Kolor


class SyntaxConverter():
    """
    converts syntax highligting theme from SublimeText to Spyder
    """
    def __init__(self, path):
        """
        :param path: path to SublimeText theme (.tmTheme file extension)
        """
        with open(path, 'rb') as fp:
            self.pl = plistlib.load(fp)

        self.name = self.pl['name']
        self.name_lowercase = self.name.lower().replace(' ', '')\
                                  .replace('(', '').replace(')', '')

        self.createSettingsDict()
        # 'foreground' key a bit misleading -> for consistency,
        # there is 'foreground' tag in .tmTheme instead of 'color'
        self.background = self.settings['background']['foreground']

        # check if theme is dark or bright
        if Kolor(self.background).luminance < 0.5:
            self.dark = True
        else:
            self.dark = False

        # relations between settings in Spyder and settings in Sublime
        # values are tuples of matching settings in desceding priority
        # (every theme defines slightly different set of tags)
        self.names_relations = {
            'background': ('background',),
            'currentline': ('lineHighlight',),
            'matched_p': ('Comment',),
            'unmatched_p': ('Keyword',),
            'ctrlclick': ('Class name', 'Inherited class', 'Function name',
                          'Entity', 'Function')
        }
        # settings with (bold, italic) options
        self.names_relations_with_options = {
            'comment': ('Comment',),
            'string': ('String',),
            'number': ('Number', 'Variable'),
            'builtin': ('Constant', 'Built-in constant',),
            'keyword': ('Keyword',),
            'definition': ('Class name', 'Inherited class', 'Function name',
                           'Entity', 'Function'),
            'normal': ('foreground',),
            'instance': ('foreground',)
            }

        # settings with no equivalents in Sublime;
        # colors derived from background color by adjusting brightness
        occurrence_coef = 0.7
        currentcell_coef = 0.95
        sideareas_coef = 0.85
        if self.dark:
            sideareas_coef = 1.05

        self.names_relations_with_luminance_change = {
            'occurrence': (('background',), occurrence_coef),
            'currentcell': (('background',), currentcell_coef),
            'sideareas': (('background',), sideareas_coef)
        }

    def createSettingsDict(self):
        """creates dictionary "settings" with color settings read from
        SublimeText theme
        """
        self.settings = dict()
        # self.settings.update(self.pl['settings'][0]['settings'])
        self.settings = {k: {'foreground': v} for (k, v)
                         in self.pl['settings'][0]['settings'].items()}

        for i in range(1, len(self.pl['settings'])):
            if 'name' in self.pl['settings'][i].keys() and\
                    'foreground' in self.pl['settings'][i]['settings'].keys():
                self.settings[self.pl['settings'][i]['name']] =\
                            self.pl['settings'][i]['settings']

    def createSpyderThemeString(self):
        self.text = ""
        self.addSettingsWithOptions()
        self.addSettings()
        self.addSettingsWithLuminanceChange()
        self.addThemeName()

    def addSettings(self):
        for key, value in self.names_relations.items():
            setting = self.findSettingInSettings(value)
            kolor = Kolor(setting['foreground'], self.background)
            self.text +=\
                self.name_lowercase + "/" + key + " = " + kolor.hex + "\n"

    def addSettingsWithOptions(self):
        for key, value in self.names_relations_with_options.items():
            setting = self.findSettingInSettings(value)
            kolor = Kolor(setting['foreground'], self.background)
            bold, italic = self.getFontStyleFromSetting(setting)
            self.text +=\
                self.name_lowercase + "/" + key + " = (\'" +\
                kolor.hex + "\', " + bold + ", " + italic + ")\n"

    def addSettingsWithLuminanceChange(self):
        for key, value in self.names_relations_with_luminance_change.items():
            setting = self.findSettingInSettings(value[0])
            kolor = Kolor(setting['foreground'], self.background)
            if self.dark:
                new_luminance = 1. - (1. - kolor.luminance) * value[1]
                kolor.luminance = new_luminance if new_luminance > 0 else 0
            else:
                kolor.luminance *= value[1]
            self.text +=\
                self.name_lowercase + "/" + key + " = " + kolor.hex + "\n"

    def addThemeName(self):
        self.text += self.name_lowercase + "/name = " + self.name + "\n"

    def findSettingInSettings(self, setting_names):
        """scans settings dict looking for keys from setting_names
        :param setting_names: tuple of keys to search for in settings
        :return: value of settings for first key which exist
        if no key is found, it raises KeyError exception
        """
        for s in setting_names:
            if s in self.settings.keys():
                return self.settings[s]
        # return self.settings['foreground']
        raise KeyError("none of these settings found in a theme: {0}"
                       .format(setting_names))

    def getFontStyleFromSetting(self, setting):
        bold, italic = 'False', 'False'
        if 'fontStyle' in setting.keys():
            if 'bold' in setting['fontStyle']:
                bold = 'True'
            if 'italic' in setting['fontStyle']:
                italic = 'True'
        return bold, italic

    def printSpyderSettings(self):
        print(self.text)

parser = argparse.ArgumentParser(
    description="""
    Convert Sublime Text syntax highligting theme (*.tmTheme) to Spyder""")
parser.add_argument('path', type=str, help='path of *.tmTheme file')
args = parser.parse_args()

sc = SyntaxConverter(args.path)
sc.createSpyderThemeString()
sc.printSpyderSettings()
