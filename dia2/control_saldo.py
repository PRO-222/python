saldo_disponible = 12500000
monto_transferencia = int (input("Ingrese monto a transferir: "))

if monto_transferencia > saldo_disponible:
    print("Saldo insuficiente")
else:
    saldo_disponible = saldo_disponible - monto_transferencia
    print("Transferencia realizada con éxito")
    print("Su saldo actual es: " + str(saldo_disponible))