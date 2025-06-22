#!/usr/bin/env python
"""
Script para ejecutar 6 pruebas unitarias automatizadas de Tienda Góngora
Ejecutar con: python run_tests.py
"""

import os
import sys
import django
from django.test.utils import get_runner
from django.conf import settings

def setup_django():
    """Configurar el entorno de Django"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tienda_gongora.settings')
    django.setup()

def run_tests():
    """Ejecutar las 6 pruebas unitarias"""
    print("🚀 Ejecutando 6 pruebas unitarias de Tienda Góngora...")
    print("=" * 60)
    
    # Configurar Django
    setup_django()
    
    # Obtener el test runner
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    
    # Ejecutar las pruebas
    failures = test_runner.run_tests(["tests"])
    
    print("=" * 60)
    if failures:
        print(f"❌ Se encontraron {failures} errores en las pruebas")
        return False
    else:
        print("✅ Las 6 pruebas pasaron exitosamente!")
        return True

def run_specific_test(test_method):
    """Ejecutar una prueba específica"""
    setup_django()
    
    test_path = f"tests.TestComponentesClave.{test_method}"
    print(f"🧪 Ejecutando prueba: {test_path}")
    
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests([test_path])
    
    if failures:
        print(f"❌ La prueba falló con {failures} errores")
        return False
    else:
        print("✅ La prueba pasó exitosamente!")
        return True

def show_test_summary():
    """Mostrar resumen de las 6 pruebas"""
    print("📋 Las 6 pruebas unitarias implementadas:")
    print("-" * 50)
    print("1. test_1_creacion_producto_con_precio")
    print("   - Valida que el producto tiene un precio asociado correctamente")
    print()
    print("2. test_2_gestion_stock_sucursal")
    print("   - Verifica que el stock de un producto está correctamente asociado a la sucursal")
    print()
    print("3. test_3_creacion_pedido_con_detalles")
    print("   - Comprueba que un detalle de pedido se relaciona bien con el producto y el pedido")
    print()
    print("4. test_4_creacion_orden_con_items")
    print("   - Verifica que el total de la orden sea el correcto")
    print()
    print("5. test_5_autenticacion_y_autorizacion")
    print("   - Verifica que un usuario autenticado puede acceder al dashboard interno")
    print()
    print("6. test_6_vista_lista_productos")
    print("   - Verifica que la vista de productos responde correctamente con filtro por categoría")
    print()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "summary":
            show_test_summary()
        elif command == "specific" and len(sys.argv) >= 3:
            test_method = sys.argv[2]
            run_specific_test(test_method)
        elif command == "help":
            print("Uso del script de pruebas:")
            print("  python run_tests.py                    - Ejecutar las 6 pruebas")
            print("  python run_tests.py summary            - Mostrar resumen de pruebas")
            print("  python run_tests.py specific test_1    - Ejecutar una prueba específica")
            print("  python run_tests.py help               - Mostrar esta ayuda")
            print()
            print("Ejemplos de pruebas específicas:")
            print("  test_1_creacion_producto_con_precio")
            print("  test_2_gestion_stock_sucursal")
            print("  test_3_creacion_pedido_con_detalles")
            print("  test_4_creacion_orden_con_items")
            print("  test_5_autenticacion_y_autorizacion")
            print("  test_6_vista_lista_productos")
        else:
            print("Comando no reconocido. Usa 'python run_tests.py help' para ver las opciones.")
    else:
        # Ejecutar las 6 pruebas
        success = run_tests()
        sys.exit(0 if success else 1) 