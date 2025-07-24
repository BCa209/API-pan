def get_cluster_label(cluster_id: int) -> str:
    """
    Devuelve la descripción del segmento correspondiente a un ID de clúster.
    """
    etiquetas: dict[int, str] = {
        0: "Compras economicas y simples",
        1: "Compras familiares de fin de semana",
        2: "Snacks de tarde"
    }
    return etiquetas.get(cluster_id, "Clúster desconocido")
