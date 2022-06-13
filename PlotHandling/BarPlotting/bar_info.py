from PlotHandling.color_handler import Color_Handler

class Bar_Info:

    def __init__(self, mean_values, error_bar_lengths, titles, bar_names, amount_of_bars, bar_config_handler, save_path):
        self.mean_values = mean_values
        self.error_bar_lengths = error_bar_lengths
        self.titles = titles
        self.bar_names = bar_names
        self.amount_of_bars = amount_of_bars
        
        plot_info = bar_config_handler.plot_info()
        self.log10 = plot_info["log_10"]

        color_handler = Color_Handler(bar_config_handler, create_n_colors = amount_of_bars)
        text_handler = color_handler.shifted_colors()
        text_background_handler = color_handler.shifted_colors(shift = -0.2)

        self.bar_colors = color_handler.get_colors()
        self.text_colors = text_handler.get_colors()
        self.text_background_colors = text_background_handler.get_colors()

        self.save_path = save_path

        self.runs = range(0, len(self.titles))

    def get_error_bar_lengths(self):
        return self.error_bar_lengths

    def get_values(self, idx):
        return (
            self.mean_values[idx], self.error_bar_lengths[idx], self.titles[idx], self.bar_names[idx],  
            self.bar_colors, self.text_colors, self.text_background_colors, self.amount_of_bars[idx], 
            self.log10, self.save_path
        ) 
    
    def amount_of_runs(self):
        return self.runs

