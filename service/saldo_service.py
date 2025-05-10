import os
from datetime import datetime

class SaldoService:
    def __init__(self, saldos_path, log_path):
        self.saldos_path = saldos_path
        self.log_path = log_path

    def get_saldo(self, username):
        print("DEBUG: Leyendo archivo de saldos en:", self.ruta_saldos)
        if not os.path.exists(self.ruta_saldos):
            print("ERROR: Archivo no encontrado.")
            return None

        with open(self.ruta_saldos, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            print("DEBUG: Contenido del archivo:")
            for line in lines:
                print(f"-> '{line.strip()}'")

            for line in lines:
                parts = line.strip().split(',')
                if len(parts) == 2 and parts[0] == username:
                    try:
                        return float(parts[1])
                    except ValueError:
                        print("ERROR: Valor inválido de saldo")
                        return None

        print(f"Usuario '{username}' no encontrado en archivo.")
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
