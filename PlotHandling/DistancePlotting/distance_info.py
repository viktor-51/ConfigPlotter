
class Distance_Info:

    def __init__(
        self, distance_values, titles, axis_names, legend_title, legend_labels, save_path 
    ):
        self.distance_values = distance_values
        
        self.titles = titles
        self.axis_names = axis_names
        self.legend_title = legend_title
        self.legend_labels = legend_labels
        
        self.save_path = save_path
        
        self.runs = range(0, len(titles))

    def get_values(self, idx):
        return (
            self.distance_values[idx], self.titles[idx], self.axis_names[idx],
            self.legend_title, self.save_path, self.legend_labels,
        ) 

    def amount_of_runs(self):
        return self.runs

