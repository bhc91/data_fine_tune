import fitz  # PyMuPDF
import re
import json
import random

def extract_legal_content(pdf_path, output_json_path):
    unwanted_text = "Ein Service des Bundesministeriums der Justiz sowie des Bundesamts für Justiz ‒ www.gesetze-im-internet.de"
    doc = fitz.open(pdf_path)
    extracted_paragraphs = []

    instructions = [
        "Ziehe den rechtlichen Inhalt aus dem angegebenen Paragraphen heraus.",
        "Entnehme den rechtlichen Inhalt aus dem genannten Abschnitt.",
        "Extrahiere die juristischen Informationen aus dem vorliegenden Paragraphen.",
        "Hol den rechtlichen Kern aus dem angegebenen Textabschnitt heraus.",
        "Isoliere den juristischen Inhalt aus dem angegebenen Absatz.",
        "Filtere den rechtlichen Gehalt aus dem benannten Paragraphen.",
        "Gewinn den juristischen Inhalt aus dem vorliegenden Abschnitt.",
        "Extrahiere die rechtlichen Details aus dem genannten Absatz.",
        "Ziehe die rechtliche Essenz aus dem angegebenen Paragraphen heraus.",
        "Entnehme die juristischen Details aus dem vorliegenden Textabschnitt.",
        "Hol die rechtliche Information aus dem genannten Paragraphen.",
        "Extrahiere die juristischen Inhalte aus dem angegebenen Abschnitt.",
        "Isoliere den rechtlichen Text aus dem benannten Absatz.",
        "Filtere den rechtlichen Inhalt aus dem vorliegenden Paragraphen.",
        "Gewinn den rechtlichen Aspekt aus dem genannten Abschnitt.",
        "Extrahiere die juristischen Details aus dem angegebenen Textabschnitt.",
        "Ziehe den rechtlichen Gehalt aus dem benannten Paragraphen heraus.",
        "Entnehme den rechtlichen Kern aus dem vorliegenden Abschnitt.",
        "Hol die juristische Information aus dem genannten Absatz heraus.",
        "Wie lautet der Inhalt und Paragraph?",
        "Kannst du mir den Inhalt des Paragraphen nennen?"
        "Extrahiere die rechtlichen Informationen aus dem angegebenen Paragraphen."
        "Ziehe den rechtlichen Inhalt aus dem angegebenen Paragraphen heraus.",
        "Entnehme den rechtlichen Inhalt aus dem genannten Abschnitt.",
        "Extrahiere die juristischen Informationen aus dem vorliegenden Paragraphen.",
        "Hol den rechtlichen Kern aus dem angegebenen Textabschnitt heraus.",
        "Isoliere den juristischen Inhalt aus dem angegebenen Absatz.",
        "Filtere den rechtlichen Gehalt aus dem benannten Paragraphen.",
        "Gewinn den juristischen Inhalt aus dem vorliegenden Abschnitt.",
        "Extrahiere die rechtlichen Details aus dem genannten Absatz.",
        "Ziehe die rechtliche Essenz aus dem angegebenen Paragraphen heraus.",
        "Entnehme die juristischen Details aus dem vorliegenden Textabschnitt.",
        "Hol die rechtliche Information aus dem genannten Paragraphen.",
        "Extrahiere die juristischen Inhalte aus dem angegebenen Abschnitt.",
        "Isoliere den rechtlichen Text aus dem benannten Absatz.",
        "Filtere den rechtlichen Inhalt aus dem vorliegenden Paragraphen.",
        "Gewinn den rechtlichen Aspekt aus dem genannten Abschnitt.",
        "Extrahiere die juristischen Details aus dem angegebenen Textabschnitt.",
        "Ziehe den rechtlichen Gehalt aus dem benannten Paragraphen heraus.",
        "Entnehme den rechtlichen Kern aus dem vorliegenden Abschnitt.",
        "Hol die juristische Information aus dem genannten Absatz heraus.",
        "Extrahiere die rechtlichen Informationen aus dem angegebenen Paragraphen.",
        "Extrahiere den rechtlichen Text aus dem genannten Paragraphen.",
        "Entnimm den juristischen Inhalt aus dem angegebenen Abschnitt.",
        "Hol die rechtlichen Informationen aus dem vorliegenden Absatz heraus.",
        "Filtere die rechtlichen Details aus dem benannten Textabschnitt.",
        "Isoliere die rechtliche Essenz aus dem angegebenen Abschnitt.",
        "Ziehe die juristischen Inhalte aus dem genannten Paragraphen heraus.",
        "Gewinn die rechtlichen Informationen aus dem vorliegenden Textabschnitt.",
        "Extrahiere den rechtlichen Kern aus dem benannten Absatz.",
        "Entnimm die juristischen Details aus dem angegebenen Paragraphen.",
        "Hol den rechtlichen Gehalt aus dem vorliegenden Abschnitt heraus.",
        "Filtere die juristische Information aus dem benannten Textabschnitt.",
        "Isoliere den rechtlichen Gehalt aus dem angegebenen Paragraphen.",
        "Extrahiere den juristischen Aspekt aus dem genannten Absatz.",
        "Ziehe die rechtlichen Details aus dem benannten Abschnitt heraus.",
        "Entnimm den rechtlichen Text aus dem vorliegenden Paragraphen.",
        "Hol die juristischen Inhalte aus dem angegebenen Abschnitt.",
        "Filtere die rechtliche Essenz aus dem benannten Paragraphen.",
        "Isoliere die rechtlichen Informationen aus dem vorliegenden Textabschnitt.",
        "Gewinn den juristischen Kern aus dem angegebenen Absatz.",
        "Extrahiere den rechtlichen Inhalt aus dem benannten Abschnitt.",
        "Ziehe die juristischen Details aus dem vorliegenden Paragraphen heraus.",
        "Entnimm den rechtlichen Gehalt aus dem genannten Textabschnitt.",
        "Hol die rechtlichen Informationen aus dem benannten Absatz heraus.",
        "Filtere die juristischen Inhalte aus dem vorliegenden Abschnitt.",
        "Isoliere den rechtlichen Kern aus dem genannten Paragraphen.",
        "Extrahiere die rechtlichen Details aus dem benannten Textabschnitt.",
        "Ziehe die juristische Information aus dem vorliegenden Absatz heraus.",
        "Gewinn den rechtlichen Text aus dem genannten Abschnitt.",
        "Entnimm die rechtlichen Informationen aus dem benannten Paragraphen.",
        "Hol die juristischen Details aus dem vorliegenden Textabschnitt."
    ]

    current_input = ""
    current_paragraph = ""
    is_bold_section = False

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict")["blocks"]
        
        skip_next = False

        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"]
                        is_bold = "bold" in span["font"].lower()

                        # Remove unwanted text and skip the next line if necessary
                        if unwanted_text in text:
                            skip_next = True
                            continue

                        if skip_next:
                            skip_next = False
                            continue

                        # Check if text starts with § and is bold
                        if re.match(r"^§\s*\d+", text) and is_bold:
                            if current_paragraph and current_input:
                                # Process the previous paragraph
                                formatted_paragraph = {
                                    "instruction": random.choice(instructions),
                                    "input": current_input.strip(),
                                    "output": current_paragraph.strip()
                                }
                                extracted_paragraphs.append(formatted_paragraph)
                                current_paragraph = ""

                            # Start a new paragraph
                            current_input = text
                            is_bold_section = True
                        elif is_bold_section and is_bold:
                            # Continue adding bold text to input
                            current_input += " " + text
                        else:
                            # Add normal text to the paragraph output
                            current_paragraph += " " + text
                            is_bold_section = False

        # Process the last paragraph in the page if it's not at the end of the document
        if current_paragraph and current_input and page_num < len(doc) - 1:
            formatted_paragraph = {
                "instruction": random.choice(instructions),
                "input": current_input.strip(),
                "output": current_paragraph.strip()
            }
            extracted_paragraphs.append(formatted_paragraph)
            current_paragraph = ""
            current_input = ""

    # Process the last paragraph in the document
    if current_paragraph and current_input:
        formatted_paragraph = {
            "instruction": random.choice(instructions),
            "input": current_input.strip(),
            "output": current_paragraph.strip()
        }
        extracted_paragraphs.append(formatted_paragraph)

    # Write the extracted paragraphs to a JSON file
    with open(output_json_path, "w", encoding="utf-8") as json_file:
        json.dump(extracted_paragraphs, json_file, ensure_ascii=False, indent=4)

# Define the paths to the input PDF and output JSON files
pdf_path = "F:/BGB.pdf"
output_json_path = "F:/LLM_Fine_Tune/bgb_alpaca_clean1.json"

# Call the function to extract legal content and save to JSON
extract_legal_content(pdf_path, output_json_path)
