"""
簡化版PDF映射器 - 使用內建字體，保證無亂碼
Simple PDF Mapper - Using built-in fonts only
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


class SimplePDFMapper:
    """Simple PDF Mapper - No font issues guaranteed"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.validation_errors = []
        
        # Create directories
        (self.project_root / "data" / "output").mkdir(parents=True, exist_ok=True)
        
        # Use only built-in fonts
        self.font_name = "Helvetica"
        self.font_bold = "Helvetica-Bold"
        
        print("Simple PDF Mapper initialized - No font issues!")
    
    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Simple validation"""
        self.validation_errors.clear()
        
        required_fields = ["patient_name", "patient_id", "date_of_birth"]
        
        for field in required_fields:
            if field not in data or not str(data[field]).strip():
                self.validation_errors.append(f"Missing required field: {field}")
        
        is_valid = len(self.validation_errors) == 0
        
        if is_valid:
            print("✓ Validation passed")
        else:
            print("✗ Validation failed:")
            for error in self.validation_errors:
                print(f"  • {error}")
        
        return is_valid
    
    def generate_simple_pdf(self, data: Dict[str, Any], output_path: str) -> bool:
        """Generate PDF using only built-in fonts"""
        try:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Create PDF
            c = canvas.Canvas(str(output_path), pagesize=letter)
            width, height = letter
            
            # Title - using only ASCII characters
            c.setFont(self.font_bold, 20)
            title = "MEDICAL FORM REPORT"
            title_width = c.stringWidth(title, self.font_bold, 20)
            c.drawString((width - title_width) / 2, height - 80, title)
            
            # Underline
            c.line(50, height - 100, width - 50, height - 100)
            
            # Basic info
            c.setFont(self.font_name, 12)
            c.drawString(50, height - 140, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            c.drawString(300, height - 140, "Version: 1.0")
            
            # Data table
            c.setFont(self.font_bold, 14)
            c.drawString(50, height - 180, "PATIENT INFORMATION")
            
            # Table data
            y_pos = height - 220
            c.setFont(self.font_name, 11)
            
            # Field mapping with English labels only
            field_labels = {
                "patient_name": "Patient Name",
                "patient_id": "Patient ID", 
                "date_of_birth": "Date of Birth",
                "gender": "Gender",
                "emergency_contact": "Emergency Contact",
                "phone": "Phone Number",
                "address": "Address",
                "insurance_number": "Insurance Number"
            }
            
            for field_name, value in data.items():
                if field_name in field_labels:
                    label = field_labels[field_name]
                    
                    # Draw label (bold)
                    c.setFont(self.font_bold, 11)
                    c.drawString(70, y_pos, f"{label}:")
                    
                    # Draw value
                    c.setFont(self.font_name, 11)
                    display_value = str(value)
                    
                    # Format boolean values
                    if isinstance(value, bool):
                        display_value = "Yes" if value else "No"
                    
                    # Limit length to prevent overflow
                    if len(display_value) > 50:
                        display_value = display_value[:47] + "..."
                    
                    c.drawString(250, y_pos, display_value)
                    
                    # Draw line under each field
                    c.line(250, y_pos - 3, 500, y_pos - 3)
                    
                    y_pos -= 30
                    
                    # New page if needed
                    if y_pos < 100:
                        c.showPage()
                        c.setFont(self.font_name, 11)
                        y_pos = height - 80
            
            # Footer
            c.setFont(self.font_name, 8)
            footer_text = "CONFIDENTIAL - This document contains Protected Health Information"
            footer_width = c.stringWidth(footer_text, self.font_name, 8)
            c.drawString((width - footer_width) / 2, 50, footer_text)
            
            c.setFont(self.font_name, 6)
            timestamp = f"Generated by PDF Mapper - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            timestamp_width = c.stringWidth(timestamp, self.font_name, 6)
            c.drawString((width - timestamp_width) / 2, 30, timestamp)
            
            c.save()
            
            print(f"✓ PDF generated successfully: {output_path}")
            print(f"  File size: {output_path.stat().st_size} bytes")
            return True
            
        except Exception as e:
            print(f"✗ PDF generation failed: {e}")
            return False
    
    def create_sample_data(self) -> Dict[str, Any]:
        """Create sample data - English only"""
        return {
            "patient_name": "John Smith",
            "patient_id": "P67890",
            "date_of_birth": "1985-03-22",
            "gender": "Male",
            "emergency_contact": True,
            "phone": "+1-555-987-6543",
            "address": "123 Main Street, Anytown, NY 12345",
            "insurance_number": "INS123456789"
        }
    
    def get_validation_errors(self) -> List[str]:
        return self.validation_errors


def run_simple_demo():
    """Run the simple demo"""
    print("=" * 60)
    print("SIMPLE PDF MAPPER DEMO")
    print("=" * 60)
    
    # Initialize
    mapper = SimplePDFMapper()
    
    # Create test cases
    test_cases = [
        {
            "name": "Standard Case",
            "data": {
                "patient_name": "Alice Johnson",
                "patient_id": "P12345",
                "date_of_birth": "1990-01-15",
                "gender": "Female",
                "emergency_contact": True,
                "phone": "+1-555-123-4567",
                "address": "456 Oak Avenue, Springfield, CA 90210",
                "insurance_number": "INS987654321"
            }
        },
        {
            "name": "Minimal Data",
            "data": {
                "patient_name": "Bob Wilson",
                "patient_id": "P99999",
                "date_of_birth": "1975-12-01",
                "gender": "Male",
                "emergency_contact": False
            }
        },
        {
            "name": "Long Text Case", 
            "data": {
                "patient_name": "Dr. Christopher Alexander Thompson Jr.",
                "patient_id": "P11111",
                "date_of_birth": "1988-06-15",
                "gender": "Male",
                "emergency_contact": True,
                "phone": "+1-555-999-8888 ext. 1234",
                "address": "789 Very Long Street Name That Goes On And On, Suite 1001, Building A, Complex B, Megacity, TX 75001-9999",
                "insurance_number": "VERY-LONG-INSURANCE-NUMBER-123456789"
            }
        }
    ]
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    successful_pdfs = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i}: {test_case['name']} ---")
        
        # Show data
        print("Data:")
        for key, value in test_case['data'].items():
            print(f"  {key}: {value}")
        
        # Validate
        if mapper.validate_data(test_case['data']):
            # Generate PDF
            pdf_filename = f"simple_demo_case_{i}_{timestamp}.pdf"
            pdf_path = f"data/output/{pdf_filename}"
            
            if mapper.generate_simple_pdf(test_case['data'], pdf_path):
                successful_pdfs.append(pdf_filename)
                print(f"✓ PDF created: {pdf_filename}")
            else:
                print(f"✗ Failed to create PDF for case {i}")
        else:
            print(f"✗ Validation failed for case {i}")
    
    # Summary
    print("\n" + "=" * 60)
    print("DEMO SUMMARY")
    print("=" * 60)
    print(f"Test cases run: {len(test_cases)}")
    print(f"Successful PDFs: {len(successful_pdfs)}")
    print(f"Output directory: {Path('data/output').absolute()}")
    
    if successful_pdfs:
        print("\nGenerated files:")
        for filename in successful_pdfs:
            file_path = Path(f"data/output/{filename}")
            if file_path.exists():
                size = file_path.stat().st_size
                print(f"  • {filename} ({size:,} bytes)")
        
        print("\n✓ All PDFs should display correctly without any font issues!")
        print("✓ Try opening them with different PDF readers to confirm")
    
    # Technical details
    print(f"\nTechnical Details:")
    print(f"  Font used: Helvetica (built-in)")
    print(f"  Page size: Letter (8.5 x 11 inches)")
    print(f"  Encoding: Standard PDF encoding")
    print(f"  No external fonts required")
    
    return len(successful_pdfs) > 0


def interactive_test():
    """Interactive testing mode"""
    print("INTERACTIVE PDF TEST MODE")
    print("=" * 40)
    
    mapper = SimplePDFMapper()
    
    while True:
        print("\nOptions:")
        print("1. Generate sample PDF")
        print("2. Create custom data PDF")
        print("3. Run full demo")
        print("4. Exit")
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == "1":
            sample_data = mapper.create_sample_data()
            print("\nUsing sample data:")
            for key, value in sample_data.items():
                print(f"  {key}: {value}")
            
            if mapper.validate_data(sample_data):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                pdf_path = f"data/output/interactive_sample_{timestamp}.pdf"
                
                if mapper.generate_simple_pdf(sample_data, pdf_path):
                    print(f"✓ Sample PDF created: {pdf_path}")
                else:
                    print("✗ Failed to create PDF")
            
        elif choice == "2":
            print("\nEnter patient data (press Enter for empty fields):")
            custom_data = {}
            
            fields = [
                "patient_name",
                "patient_id", 
                "date_of_birth",
                "gender",
                "phone",
                "address"
            ]
            
            for field in fields:
                value = input(f"{field}: ").strip()
                if value:
                    # Convert boolean-like strings
                    if value.lower() in ['true', 'yes', '1']:
                        custom_data[field] = True
                    elif value.lower() in ['false', 'no', '0']:
                        custom_data[field] = False
                    else:
                        custom_data[field] = value
            
            if mapper.validate_data(custom_data):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                pdf_path = f"data/output/interactive_custom_{timestamp}.pdf"
                
                if mapper.generate_simple_pdf(custom_data, pdf_path):
                    print(f"✓ Custom PDF created: {pdf_path}")
                else:
                    print("✗ Failed to create PDF")
        
        elif choice == "3":
            run_simple_demo()
        
        elif choice == "4":
            print("Goodbye!")
            break
        
        else:
            print("Invalid option, please try again.")


if __name__ == "__main__":
    print("SIMPLE PDF MAPPER - NO FONT ISSUES GUARANTEED")
    print("=" * 60)
    
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_test()
    else:
        success = run_simple_demo()
        
        if success:
            print("\n🎉 Demo completed successfully!")
            print("📁 Check the data/output folder for PDF files")
            print("💡 All text should display perfectly without any font issues")
        else:
            print("\n❌ Demo had some issues")