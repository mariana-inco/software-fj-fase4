def simulacion():
    gestor = GestorReservas()

    operaciones = []

    try:
        cliente1 = Cliente("Juan Perez", "123456")
        cliente2 = Cliente("Maria Lopez", "789456")

        servicio1 = SalaReuniones("Sala A", 50000)
        servicio2 = AlquilerEquipo("Portatil", 30000)
        servicio3 = AsesoriaEspecializada("Python", 80000)

        operaciones.extend([
            (cliente1, servicio1, 2),
            (cliente2, servicio2, 1),
            (cliente1, servicio3, 3),
            (cliente2, servicio1, 4),
            (cliente1, servicio2, 5),
        ])

    except Exception as e:
        logging.error(f"Error creando datos iniciales: {e}")

    for cliente, servicio, duracion in operaciones:

        try:
            reserva = Reserva(cliente, servicio, duracion)

            reserva.confirmar()
            reserva.procesar()

            gestor.agregar_reserva(reserva)

            print("Reserva exitosa:", reserva)

        except Exception as e:
            logging.error(f"Reserva fallida: {e}")

    # Casos incorrectos

    casos_erroneos = [
        (None, servicio1, 2),
        (cliente1, None, 2),
        (cliente1, servicio1, -5),
        (cliente1, servicio1, 0),
        (cliente1, servicio1, 1)
    ]

    for cliente, servicio, duracion in casos_erroneos:

        try:
            reserva = Reserva(cliente, servicio, duracion)

            reserva.procesar()

        except Exception as e:
            logging.error(f"Error controlado: {e}")
            print("Error capturado:", e)

    print(
        f"Total reservas almacenadas: "
        f"{len(gestor.listar_reservas())}"
    )