"""
Analyze extracted Access database data and create real data for SQLite
"""
import pandas as pd
import os
from pathlib import Path

def analyze_extracted_data():
    """Analyze the extracted CSV files"""
    extracted_dir = Path("extracted_data")
    
    if not extracted_dir.exists():
        print("❌ extracted_data directory not found")
        return
    
    # Key tables for Open Orders functionality
    key_tables = {
        'OO_ReportData.csv': 'Main Open Orders Report Data',
        'tblShipmentStatus.csv': 'Shipment Status Information', 
        'tNewOrderReceived.csv': 'New Orders Received',
        '011OORptData_Step1.csv': 'Open Order Report Step 1',
        'APHDR.csv': 'AP Header (likely orders)',
        'APDIST.csv': 'AP Distribution (likely order details)'
    }
    
    print("=== ANALYZING EXTRACTED ACCESS DATABASE DATA ===\n")
    
    for filename, description in key_tables.items():
        filepath = extracted_dir / filename
        if filepath.exists():
            try:
                df = pd.read_csv(filepath)
                print(f"📋 {filename} - {description}")
                print(f"   Rows: {len(df)}")
                print(f"   Columns: {list(df.columns)}")
                
                if len(df) > 0:
                    print("   Sample data:")
                    print(f"   {df.head(1).to_string(index=False)}")
                else:
                    print("   ⚠️ No data in this table")
                print()
                
            except Exception as e:
                print(f"❌ Error reading {filename}: {e}")
        else:
            print(f"❌ {filename} not found")
    
    # Check all available files
    print("\n=== ALL EXTRACTED FILES ===")
    csv_files = list(extracted_dir.glob("*.csv"))
    for csv_file in sorted(csv_files):
        try:
            df = pd.read_csv(csv_file)
            print(f"📄 {csv_file.name}: {len(df)} rows, {len(df.columns)} columns")
        except Exception as e:
            print(f"❌ {csv_file.name}: Error - {e}")

if __name__ == "__main__":
    analyze_extracted_data()
