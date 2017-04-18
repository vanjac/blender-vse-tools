from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter import colorchooser
import webbrowser
import html

def generateCSS(rules):
    """
    Generate CSS from a list of rules, each with a selector and list of
    declarations.
    :param rules: a list of 2-tuples: (selector, declarations) where
    declarations is a dictionary.
    :return: CSS as a string
    """
    css = [ ]
    for rule in rules:
        selector = rule[0]
        declarations = rule[1]
        css.append(selector)
        css.append(' {\n')
        for property, value in declarations.items():
            css.append('    ')
            css.append(property)
            css.append(': ')
            css.append(str(value))
            css.append(';\n')
        css.append('}\n\n')
    return ''.join(css)

# https://www.w3schools.com/cssref/css_websafe_fonts.asp
fonts = [
    'Georgia, serif',
    '"Palatino Linotype", "Book Antiqua", Palatino, serif',
    '"Times New Roman", Times, serif',
    'Arial, Helvetica, sans-serif',
    '"Arial Black", Gadget, sans-serif',
    '"Comic Sans MS", cursive, sans-serif',
    'Impact, Charcoal, sans-serif',
    '"Lucida Sans Unicode", "Lucida Grande", sans-serif',
    'Tahoma, Geneva, sans-serif',
    '"Trebuchet MS", Helvetica, sans-serif',
    'Verdana, Geneva, sans-serif',
    '"Courier New", Courier, monospace',
    '"Lucida Console", Monaco, monospace'
]


class TitlerApp:

    def __init__(self, root):
        self.file = open('title.html', 'w')
        self.ready = False

        self.root = root

        frame = Frame(root)
        frame.pack(side=TOP, fill=BOTH, expand=True)

        Grid.columnconfigure(frame, 0, weight=1)

        row = 0

        openBrowserButton = Button(frame, text="Open Browser",
                                   command=self._openBrowser)
        openBrowserButton.grid(row=row, sticky=W)
        row += 1

        self.textBox = ScrolledText(frame, width=40, height=10)
        self.textBox.grid(row=row, sticky=N+S+E+W)
        self.textBox.bind_all('<<Modified>>', self.updateFile)
        row += 1

        propertiesFrame = Frame(frame)
        propertiesFrame.grid(row=row, sticky=E+W)
        self._makePropertiesFrame(propertiesFrame)

    def _makePropertiesFrame(self, frame):
        #Grid.columnconfigure(frame, 0, weight=1)
        Grid.columnconfigure(frame, 1, weight=1)

        row = 0

        self.textColor = "#ffffff"
        self.backgroundColor = "#000000"

        textColorLabel = Label(frame, text="Text color:")
        textColorLabel.grid(row=row, column=0, sticky=E)

        self.textColorButton = Button(frame, width=5,
                                      command=self._pickTextColor)
        self.textColorButton.grid(row=row, column=1, sticky=W)
        row += 1

        backgroundColorLabel = Label(frame, text="Background color:")
        backgroundColorLabel.grid(row=row, column=0, sticky=E)

        self.backgroundColorButton = Button(frame, width=5,
                                            command=self._pickBackgroundColor)
        self.backgroundColorButton.grid(row=row, column=1, sticky=W)
        row += 1

        fontLabel = Label(frame, text="Font:")
        fontLabel.grid(row=row, column=0, sticky=E)

        self.fontVar = StringVar()
        self.fontVar.set(fonts[0])
        fontOptionMenu = \
            OptionMenu(*([frame, self.fontVar]
                         + fonts))
        fontOptionMenu.grid(row=row, column=1, sticky=W)
        self.fontVar.trace(mode="w", callback=self.updateFile)
        row += 1

        fontSizeLabel = Label(frame, text="Font size:")
        fontSizeLabel.grid(row=row, column=0, sticky=E)

        # has to be self. , otherwise it will be garbage collected
        self.fontSizeVar = StringVar()
        fontSizeBox = Spinbox(frame, from_=0, to=65536, width=5,
                              textvariable=self.fontSizeVar)
        fontSizeBox.grid(row=row, column=1, sticky=W)
        self.fontSizeVar.set('12')
        self.fontSizeVar.trace(mode="w", callback=self.updateFile)
        row += 1

        letterSpacingLabel = Label(frame, text="Letter spacing:")
        letterSpacingLabel.grid(row=row, column=0, sticky=E)

        self.letterSpacingVar = StringVar()
        letterSpacingBox = Spinbox(frame, from_=-999, to=999, width=5,
                                   textvariable=self.letterSpacingVar)
        letterSpacingBox.grid(row=row, column=1, sticky=W)
        self.letterSpacingVar.set('0')
        self.letterSpacingVar.trace(mode="w", callback=self.updateFile)
        row += 1

        wordSpacingLabel = Label(frame, text="Word spacing:")
        wordSpacingLabel.grid(row=row, column=0, sticky=E)

        self.wordSpacingVar = StringVar()
        wordSpacingBox = Spinbox(frame, from_=-999, to=999, width=5,
                                 textvariable=self.wordSpacingVar)
        wordSpacingBox.grid(row=row, column=1, sticky=W)
        self.wordSpacingVar.set('0')
        self.wordSpacingVar.trace(mode="w", callback=self.updateFile)
        row += 1

        lineHeightLabel = Label(frame, text="Line height:")
        lineHeightLabel.grid(row=row, column=0, sticky=E)

        self.lineHeightVar = StringVar()
        lineHeightBox = Spinbox(frame, from_=0, to=9999, width=5,
                                textvariable=self.lineHeightVar)
        lineHeightBox.grid(row=row, column=1, sticky=W)
        self.lineHeightVar.set('100')
        self.lineHeightVar.trace(mode="w", callback=self.updateFile)
        row += 1

        paragraphMarginLabel = Label(frame, text="Paragraph break height:")
        paragraphMarginLabel.grid(row=row, column=0, sticky=E)

        self.paragraphMarginVar = StringVar()
        paragraphMarginBox = Spinbox(frame, from_=0, to=9999, width=5,
                                     textvariable=self.paragraphMarginVar)
        paragraphMarginBox.grid(row=row, column=1, sticky=W)
        self.paragraphMarginVar.set('0')
        self.paragraphMarginVar.trace(mode="w", callback=self.updateFile)
        row += 1

        textAlignLabel = Label(frame, text="Text align:")
        textAlignLabel.grid(row=row, column=0, sticky=E)

        self.textAlignVar = StringVar()
        Radiobutton(frame, text="Left", variable=self.textAlignVar,
                    value="left", command=self.updateFile)\
            .grid(row=row, column=1, sticky=W)
        row += 1
        Radiobutton(frame, text="Center", variable=self.textAlignVar,
                    value="center", command=self.updateFile)\
            .grid(row=row, column=1, sticky=W)
        row += 1
        Radiobutton(frame, text="Right", variable=self.textAlignVar,
                    value="right", command=self.updateFile)\
            .grid(row=row, column=1, sticky=W)
        row += 1
        Radiobutton(frame, text="Justify", variable=self.textAlignVar,
                    value="justify", command=self.updateFile)\
            .grid(row=row, column=1, sticky=W)
        row += 1
        self.textAlignVar.set('left')

        fontWeightLabel = Label(frame, text="Font weight:")
        fontWeightLabel.grid(row=row, column=0, sticky=E)

        fontWeightFrame = Frame(frame)
        fontWeightFrame.grid(row=row, column=1, sticky=W)

        self.fontWeightVar = StringVar()
        self.fontWeightBox = Spinbox(fontWeightFrame, from_=1, to=9, width=5,
                                     textvariable=self.fontWeightVar)
        self.fontWeightBox.pack(side=LEFT)
        self.fontWeightVar.set('4')
        self.fontWeightVar.trace(mode="w", callback=self.updateFile)

        fontWeightValuesLabel = Label(fontWeightFrame,
                                      text="1 - 9; 4: Normal, 7: Bold")
        fontWeightValuesLabel.pack(side=LEFT)
        row += 1

        self.italicsVar = IntVar()
        italicsLabel = Label(frame, text="Italics:")
        italicsLabel.grid(row=row, column=0, sticky=E)
        italicsCheckbutton = Checkbutton(frame, command=self.updateFile,
                             variable=self.italicsVar)
        italicsCheckbutton.grid(row=row, column=1, sticky=W)
        row += 1

        self.underlineVar = IntVar()
        underlineLabel = Label(frame, text="Underline:")
        underlineLabel.grid(row=row, column=0, sticky=E)
        underlineCheckbutton = Checkbutton(frame, command=self.updateFile,
                               variable=self.underlineVar)
        underlineCheckbutton.grid(row=row, column=1, sticky=W)
        row += 1

        self.strikethroughVar = IntVar()
        strikethroughLabel = Label(frame, text="Strikethrough:")
        strikethroughLabel.grid(row=row, column=0, sticky=E)
        strikethroughCheckbutton = Checkbutton(frame, command=self.updateFile,
                                   variable=self.strikethroughVar)
        strikethroughCheckbutton.grid(row=row, column=1, sticky=W)
        row += 1

        capsModeLabel = Label(frame, text="Caps:")
        capsModeLabel.grid(row=row, column=0, sticky=E)

        self.capsModeVar = StringVar()
        Radiobutton(frame, text="Normal", variable=self.capsModeVar,
                    value="normal", command=self.updateFile) \
            .grid(row=row, column=1, sticky=W)
        row += 1
        Radiobutton(frame, text="ALL CAPS", variable=self.capsModeVar,
                    value="upper", command=self.updateFile) \
            .grid(row=row, column=1, sticky=W)
        row += 1
        Radiobutton(frame, text="all lowercase", variable=self.capsModeVar,
                    value="lower", command=self.updateFile) \
            .grid(row=row, column=1, sticky=W)
        row += 1
        Radiobutton(frame, text="Small Caps", variable=self.capsModeVar,
                    value="small", command=self.updateFile) \
            .grid(row=row, column=1, sticky=W)
        row += 1
        self.capsModeVar.set("normal")

        self.ready = True
        self.updateFile()

    def _pickTextColor(self):
        color = colorchooser.askcolor()[1]
        if color is not None:
            self.textColor = color
            self.updateFile()

    def _pickBackgroundColor(self):
        color = colorchooser.askcolor()[1]
        if color is not None:
            self.backgroundColor = color
            self.updateFile()

    def _openBrowser(self):
        webbrowser.open(self.file.name)

    def updateFile(self, *args, **kwargs):
        # update gui
        self.textColorButton.configure(background=self.textColor)
        self.backgroundColorButton.configure(background=self.backgroundColor)

        self._updateFileRaw()
        self._updateFileRaw()

    def _updateFileRaw(self):
        if not self.ready:
            return
        self.file.truncate()
        self.file.seek(0)

        rules = [
            ('*', {
                'margin': '0pt',
                'padding': '0pt'
            }),
            ('body', {
                'background-color': self.backgroundColor,
            }),
            ('pre', {
                'color': self.textColor,
                'font-family': self.fontVar.get(),
                'font-size': self.fontSizeVar.get() + 'pt',
                'letter-spacing': self.letterSpacingVar.get() + 'pt',
                'word-spacing': self.wordSpacingVar.get() + 'pt',
                'line-height': self.lineHeightVar.get() + '%',
                'margin-bottom': self.paragraphMarginVar.get() + 'pt',
                'text-align': self.textAlignVar.get(),
                'font-weight': int(self.fontWeightVar.get()) * 100,
                'font-style': "italic" if self.italicsVar.get()==1 \
                    else "normal",
                'text-decoration':
                    ("underline " if self.underlineVar.get()==1 else "") \
                  + ("line-through " if self.strikethroughVar.get()==1 else ""),
                'font-variant': \
                    "small-caps" if self.capsModeVar.get() == "small" \
                    else "normal"
            })
        ]

        styleStr = generateCSS(rules)

        htmlStr = \
"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
{style}
</style>
</head>
<body>
<pre>
{text}
</pre>
</body>
</html>
"""

        text = self.textBox.get("1.0", END)
        if self.capsModeVar.get() == "upper":
            text = text.upper()
        elif self.capsModeVar.get() == "lower":
            text = text.lower()
        text = html.escape(text)
        text = text.replace('\n\n', '</pre><pre>')
        text = text.replace('\n', '<br>')
        htmlStr = htmlStr.format(style=styleStr,
                                 text=text)

        self.file.write(htmlStr)

        self.textBox.edit_modified(0) # allow <<Modified>> event to run again

if __name__ == "__main__":
    root = Tk()
    root.resizable(True, False)
    app = TitlerApp(root)
    root.mainloop()
    app.file.close()
