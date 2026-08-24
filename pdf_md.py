import os
import sys
import subprocess
import pdf_inspector

def extract_pdf_to_md(pdf_path: str, output_md_path: str = None) -> str:
    """
    Fast PDF to Markdown extraction.
    Uses pdf-inspector for text-based PDFs.
    Falls back to macOS native Vision OCR for scanned/image-based PDFs.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
    result = pdf_inspector.process_pdf(pdf_path)
    md_content = result.markdown or ""
    
    # Fallback to macOS Vision OCR if pdf is scanned/image-based or markdown is empty
    if not md_content.strip() or result.pdf_type in ["scanned", "image_based"]:
        print(f"[{result.pdf_type}] Using macOS Vision OCR for scanning/image extraction...")
        swift_code = f"""
import Foundation
import PDFKit
import Vision
import AppKit

let file = "{pdf_path}"
guard let doc = PDFDocument(url: URL(fileURLWithPath: file)) else {{ exit(1) }}

func ocrPage(_ page: PDFPage) -> String {{
    let rect = page.bounds(for: .mediaBox)
    let width = Int(rect.width * 2.0)
    let height = Int(rect.height * 2.0)
    guard width > 0, height > 0 else {{ return "" }}
    let colorSpace = CGColorSpaceCreateDeviceRGB()
    let bitmapInfo = CGImageAlphaInfo.premultipliedLast.rawValue
    guard let context = CGContext(data: nil, width: width, height: height, bitsPerComponent: 8, bytesPerRow: width * 4, space: colorSpace, bitmapInfo: bitmapInfo) else {{ return "" }}
    context.setFillColor(NSColor.white.cgColor)
    context.fill(CGRect(x: 0, y: 0, width: width, height: height))
    context.saveGState()
    context.scaleBy(x: 2.0, y: 2.0)
    page.draw(with: .mediaBox, to: context)
    context.restoreGState()
    guard let cgImage = context.makeImage() else {{ return "" }}
    let requestHandler = VNImageRequestHandler(cgImage: cgImage, options: [:])
    let request = VNRecognizeTextRequest()
    request.recognitionLevel = .accurate
    request.recognitionLanguages = ["ko-KR", "en-US"]
    request.usesLanguageCorrection = true
    do {{
        try requestHandler.perform([request])
        guard let observations = request.results else {{ return "" }}
        return observations.compactMap {{ $0.topCandidates(1).first?.string }}.joined(separator: "\\n")
    }} catch {{ return "" }}
}}

for i in 0..<doc.pageCount {{
    if let page = doc.page(at: i) {{
        let text = ocrPage(page)
        print("## Page \\(i + 1)\\n")
        print(text)
        print("\\n")
    }}
}}
"""
        res = subprocess.run(["swift", "-"], input=swift_code, text=True, capture_output=True)
        if res.returncode == 0 and res.stdout.strip():
            md_content = res.stdout
            
    if output_md_path:
        with open(output_md_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        print(f"Saved Markdown to {output_md_path}")
        
    return md_content

if __name__ == "__main__":
    # Check command line arguments first
    if len(sys.argv) > 1:
        pdf_input = sys.argv[1].strip("'\" ")
    else:
        pdf_input = input("변환할 PDF 파일 경로를 입력하세요: ").strip("'\" ")
        
    if not pdf_input:
        print("오류: 파일 경로가 입력되지 않았습니다.")
        sys.exit(1)
        
    pdf_path = os.path.abspath(pdf_input)
    if not os.path.exists(pdf_path):
        print(f"오류: 파일을 찾을 수 없습니다: {pdf_path}")
        sys.exit(1)
        
    # Auto-generate output filename (.pdf -> .md)
    base_name, _ = os.path.splitext(pdf_path)
    output_file = f"{base_name}.md"
    
    markdown_text = extract_pdf_to_md(pdf_path, output_file)
    print(f"\n성공적으로 변환되었습니다 -> {output_file}")