from web_crawler.formatter.writers import YAMLOutput, FileOutput


class OutputStream:

    @staticmethod
    def get_writer(format_option):
        if format_option == 'yaml':
            return YAMLOutput
        if format_option == 'file':
            return FileOutput
