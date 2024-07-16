class Heading:
    def __init__(self, title):
        self.title = title
        self.headings = []
        self.text = ""

    def add_heading(self, heading):
        self.headings.append(heading)

    def add_text(self, text):
        self.text += text + "\n"

    def __str__(self):
        result = f"Heading: {self.title}\n"
        if self.text:
            result += self.text + "\n"
        for heading in self.headings:
            result += str(heading)
        return result

class DocumentParser:
    def __init__(self):
        self.headings = []
        self.current_heading = None

    def parse_document(self, document):
        lines = document.splitlines()

        for line in lines:
            line = line.rstrip()  # Remove trailing whitespace
            if line.isupper():
                # This is a heading
                self.current_heading = Heading(line)
                self.headings.append(self.current_heading)
            elif line.startswith("    "):
                # This is a subheading (nested heading)
                if self.current_heading:
                    nested_heading = Heading(line.lstrip())
                    self.current_heading.add_heading(nested_heading)
                    self.current_heading = nested_heading
                else:
                    # Handling subheadings without a preceding heading (if any)
                    self.current_heading = Heading("Untitled Heading")  # Or handle differently as needed
                    nested_heading = Heading(line.lstrip())
                    self.current_heading.add_heading(nested_heading)
                    self.headings.append(self.current_heading)
                    self.current_heading = nested_heading
            else:
                # This is text within the current heading or subheading
                if self.current_heading:
                    self.current_heading.add_text(line)

    def __str__(self):
        result = ""
        for heading in self.headings:
            result += str(heading)
        return result
