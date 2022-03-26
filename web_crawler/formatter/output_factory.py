from web_crawler.formatter.writers import YAMLOutput, FileOutput


class OutputStream:

    @staticmethod
    def get_formatter(format_option):
        if format_option == 'yaml':
            return YAMLOutput()

    @staticmethod
    def get_writer(output_dir):
        return FileOutput(output_dir)
