import PyPDF2
import pdfplumber

def extraer_texto_pdf(archivo_pdf):
    """Extrae texto de un archivo PDF usando pdfplumber"""
    texto_completo = ""
    
    try:
        with pdfplumber.open(archivo_pdf) as pdf:
            print(f"📄 Extrayendo texto de: {archivo_pdf}")
            print(f"📖 Total de páginas: {len(pdf.pages)}")
            
            for i, pagina in enumerate(pdf.pages, 1):
                texto_pagina = pagina.extract_text()
                if texto_pagina:
                    texto_completo += f"\n\n=== PÁGINA {i} ===\n"
                    texto_completo += texto_pagina
                    
            return texto_completo
            
    except Exception as e:
        print(f"❌ Error al extraer texto: {e}")
        return None

if __name__ == "__main__":
    archivo = "Reto_IA_IBM_Senasoft_2025_ArteFinal.pdf"
    texto = extraer_texto_pdf(archivo)
    
    if texto:
        # Guardar el texto extraído
        with open("contenido_reto_senasoft.txt", "w", encoding="utf-8") as f:
            f.write(texto)
        
        print("✅ Texto extraído y guardado en 'contenido_reto_senasoft.txt'")
        
        # Mostrar las primeras líneas para verificar
        print("\n" + "="*60)
        print("VISTA PREVIA DEL CONTENIDO:")
        print("="*60)
        print(texto[:2000] + "..." if len(texto) > 2000 else texto)
    else:
        print("❌ No se pudo extraer el texto del PDF")