import argparse
from generator import generator


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generar un script con código predefinido.")
    parser.add_argument("file_name", help="Nombre del archivo de script a generar")
    parser.add_argument("to")
    args = parser.parse_args()
    if args.to == "operations":
        generator.generate_operations(args.file_name)
    else:
        generator.generate_create_update_operation(args.file_name)
