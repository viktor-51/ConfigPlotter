
class Line_Info:

    def __init__(
        self, mean_values, std_values, titles, axis_names, legend_title, legend_labels, save_path,
        time = None
    ):
        self.mean_values = mean_values
        self.std_values = std_values

        self.titles = titles
        self.axis_names = axis_names
        self.legend_title = legend_title
        self.legend_labels = legend_labels
        
        self.save_path = save_path
        self.time = time

        self.runs = range(0, len(titles))

    def get_values(self, idx):
        return (
            self.mean_values[idx], self.titles[idx], self.axis_names[idx], 
            self.legend_title, self.save_path, self.next_time(idx), self.std_values[idx],
            self.legend_labels
        ) 

    def next_time(self, idx):
        if self.time is None: 
            return None 
        else: 
            return self.time[idx]

    def amount_of_runs(self):
        return self.runs

