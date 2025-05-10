import os
from datetime import datetime

class SaldoService:
    def __init__(self, ruta_saldos, ruta_log):
        self.ruta_saldos = ruta_saldos
        self.ruta_log = ruta_log

    def get_saldo(self, username):
        print(f"DEBUG: Buscando saldo para '{username}'")
        print("DEBUG: Ruta del archivo:", self.ruta_saldos)

        if not os.path.exists(self.ruta_saldos):
            print("ERROR: Archivo no existe.")
            return None

        try:
            with open(self.ruta_saldos, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                print("DEBUG: Contenido del archivo:")
                for i, line in enumerate(lines):
                    print(f"Línea {i + 1}: '{line.strip()}'")

                for line in lines:
                    parts = line.strip().split(',')
                    if len(parts) == 2:
                        nombre, saldo_str = parts
                        print(f"-> Comparando '{nombre}' con '{username}'")
                        if nombre == username:
                            saldo = float(saldo_str.strip())
                            print(f"Encontrado: {nombre} con saldo {saldo}")
                            return saldo
                    else:
                        print(f"Formato inválido en línea: '{line.strip()}'")

        except Exception as e:
            print("ERROR durante lectura del archivo:", str(e))

        print(f"Usuario '{username}' no encontrado.")
        return None

    def update_saldo(self, username, nuevo_saldo):
        if not os.path.exists(self.saldos_path):
            return False

        actualizado = False
        lineas = []
        with open(self.saldos_path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) == 2 and parts[0] == username:
                    lineas.append(f"{username},{nuevo_saldo}\n")
                    actualizado = True
                else:
                    lineas.append(line)

        if actualizado:
            with open(self.saldos_path, 'w', encoding='utf-8') as f:
                f.writelines(lineas)
            return True
        return False

    def registrar_log(self, username, accion, monto):
        fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_line = f"{fecha} - {username} - {accion} - {monto}\n"
        with open(self.log_path, 'a', encoding='utf-8') as f:
            f.write(log_line)

    def ingresar(self, username, monto):
        saldo_actual = self.get_saldo(username)
        if saldo_actual is None:
            return False
        nuevo_saldo = saldo_actual + monto
        if self.update_saldo(username, nuevo_saldo):
            self.registrar_log(username, "ingreso", monto)
            return True
        return False

    def retirar(self, username, monto):
        saldo_actual = self.get_saldo(username)
        if saldo_actual is None or saldo_actual < monto:
            return False
        nuevo_saldo = saldo_actual - monto
        if self.update_saldo(username, nuevo_saldo):
            self.registrar_log(username, "retiro", monto)
            return True
        return False
