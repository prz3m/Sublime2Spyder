# Sublime2Spyder

Converting Sublime Text syntax highlighting theme to [Spyder](https://github.com/spyder-ide/spyder).

You can find a lot of Sublime themes at [Colorsublime](http://colorsublime.com/).

#Usage

1. Open terminal and run script with command: 
   `python sublime2spyder.py sublimetheme.tmTheme`
2. Copy the output.
3. Close Spyder.
4. Open spyder.ini file (location in Windows: C:/Users/%USERNAME/.spyder-py3 or similar).
5. Find `[color_schemes]` section.
6. Make sure that the name of converted theme doesn't overlap with one of Spyder's default themes (if there are 2 lines with the same setting in spyder.ini, Spyder can't run). Paste the output in `[color_schemes]` section.
7. Add your theme's name in `names` list
  (look for `names = ['emacs', 'idle', 'monokai', 'pydev', 'scintilla', 'spyder', 'spyder/dark', 'zenburn']` line).
8. Run Spyder, go to Preferences -> Syntax coloring, select your theme and that's all!

# Examples

Here is [Solarized dark](http://colorsublime.com/theme/Solarized-dark) theme in Spyder:

![Solarized dark](/../screenshots/solarizeddark.png?raw=true)
