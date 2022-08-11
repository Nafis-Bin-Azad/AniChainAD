try:
    import Tkinter as tk
    import tkFont
    import ttk
    import app as appData
except ImportError:  # Python 3
    import tkinter as tk
    import tkinter.font as tkFont
    import tkinter.ttk as ttk
    import app as appData


class MultiColumnListbox(object):

    def __init__(self):
        self.label = None
        self.input = None
        self.tree = None
        self._setup_widgets()
        self._build_tree()

    def _setup_widgets(self):

        container = ttk.Frame()
        container.pack(fill='both', expand=True)

        self.label = ttk.Label(text="Search Anime: ")
        self.label.grid(row=0, column=0, in_=container)

        self.input = ttk.Entry()
        self.input.grid(row=0, column=1, in_=container)

        # create a treeview with dual scrollbars
        self.tree = ttk.Treeview(columns=title_header, show="headings")
        vsb = ttk.Scrollbar(orient="vertical",
                            command=self.tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal",
                            command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set,
                            xscrollcommand=hsb.set)
        self.tree.grid(row=1, column=0, columnspan=2,
                       in_=container, sticky='nsew')
        self.tree.bind("<<TreeviewSelect>>", self.OnSelect)
        vsb.grid(row=0, column=2, sticky='ns', in_=container, rowspan=2)
        hsb.grid(row=2, column=0,  sticky='ew', in_=container)
        container.grid_rowconfigure(1, weight=2)
        container.grid_columnconfigure(1, weight=2)

    def _build_tree(self):
        for col in title_header:
            self.tree.heading(col, text=col.title(),
                              command=lambda c=col: sortby(self.tree, c, 0))
            # adjust the column's width to the header string
            self.tree.column(col,
                             width=tkFont.Font().measure(col.title()))

        for item in data_list:
            self.tree.insert('', 'end', values=item)
            # adjust column's width if necessary to fit each value
            for ix, val in enumerate(item):
                col_w = tkFont.Font().measure(val)
                if self.tree.column(title_header[ix], width=None) < col_w:
                    self.tree.column(title_header[ix], width=col_w)

    def OnSelect(self, event):
        item = self.tree.selection()[0]
        animeTitle = self.tree.item(item, "values")[1]
        # appData.downloadAnime(animeTitle)


def sortby(tree, col, descending):
    # Sort tree contents when a column header is clicked on
    # grab values to sort
    data = [(tree.set(child, col), child)
            for child in tree.get_children('')]
    # if the data to be sorted is numeric change to float
    # data =  change_numeric(data)
    # now sort the data in place
    data.sort(reverse=descending)
    for ix, item in enumerate(data):
        tree.move(item[1], '', ix)
    # switch the heading so it will sort in the opposite direction
    tree.heading(col, command=lambda col=col: sortby(tree, col,
                                                     int(not descending)))


# Data to be displayed in the listbox
title_header = ['Date', 'Title']
data_list = appData.animeList


if __name__ == '__main__':
    root = tk.Tk()
    root.title("AniChainAD")
    root.attributes("-fullscreen", True)
    listbox = MultiColumnListbox()
    root.mainloop()
