import logging
from datetime import datetime


def aplicar_config_dinamica_segura(
    config_atual, nova_config, log_path="neat_dinamico.log"
):
    """
    Compara duas configurações NEAT e aplica mudanças dinâmicas seguras,
    registrando tudo no console e em arquivo de log.
    """

    # Setup do logger
    logger = logging.getLogger("NEAT-Dinamico")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    logger.info("======== INÍCIO DA ATUALIZAÇÃO DINÂMICA ========")
    logger.info(f"Horário: {datetime.now()}")

    # GENOME CONFIG
    g_atual = config_atual.genome_config
    g_novo = nova_config.genome_config

    atributos_seguro_genome = [
        "node_add_prob",
        "node_delete_prob",
        "conn_add_prob",
        "conn_delete_prob",
        "weight_mutate_power",
        "weight_mutate_rate",
        "weight_replace_rate",
        "bias_mutate_power",
        "bias_mutate_rate",
        "bias_replace_rate",
        "response_mutate_power",
        "response_mutate_rate",
        "response_replace_rate",
        "enabled_mutate_rate",
        "weight_min_value",
        "weight_max_value",
        "bias_min_value",
        "bias_max_value",
        "response_min_value",
        "response_max_value",
        "compatibility_disjoint_coefficient",
        "compatibility_weight_coefficient",
    ]

    for attr in atributos_seguro_genome:
        val_antigo = getattr(g_atual, attr, None)
        val_novo = getattr(g_novo, attr, None)
        if val_novo is not None and val_antigo != val_novo:
            setattr(g_atual, attr, val_novo)
            msg = f"[GENOME] {attr}: {val_antigo} -> {val_novo}"
            print(msg)
            logger.info(msg)

    # SPECIES CONFIG
    s_atual = config_atual.species_set_config
    s_novo = nova_config.species_set_config
    attr = "compatibility_threshold"
    val_antigo = getattr(s_atual, attr, None)
    val_novo = getattr(s_novo, attr, None)
    if val_novo is not None and val_antigo != val_novo:
        setattr(s_atual, attr, val_novo)
        msg = f"[SPECIES] {attr}: {val_antigo} -> {val_novo}"
        print(msg)
        logger.info(msg)

    # STAGNATION CONFIG
    stagn_atual = config_atual.stagnation_config
    stagn_novo = nova_config.stagnation_config
    for attr in ["species_elitism", "max_stagnation", "species_fitness_func"]:
        val_antigo = getattr(stagn_atual, attr, None)
        val_novo = getattr(stagn_novo, attr, None)
        if val_novo is not None and val_antigo != val_novo:
            setattr(stagn_atual, attr, val_novo)
            msg = f"[STAGNATION] {attr}: {val_antigo} -> {val_novo}"
            print(msg)
            logger.info(msg)

    # REPRODUCTION CONFIG
    r_atual = config_atual.reproduction_config
    r_novo = nova_config.reproduction_config
    for attr in ["elitism", "survival_threshold", "min_species_size"]:
        val_antigo = getattr(r_atual, attr, None)
        val_novo = getattr(r_novo, attr, None)
        if val_novo is not None and val_antigo != val_novo:
            setattr(r_atual, attr, val_novo)
            msg = f"[REPRODUCTION] {attr}: {val_antigo} -> {val_novo}"
            print(msg)
            logger.info(msg)

    # MAIN NEAT CONFIG
    for attr in ["fitness_threshold", "reset_on_extinction", "pop_size"]:
        val_antigo = getattr(config_atual, attr, None)
        val_novo = getattr(nova_config, attr, None)
        if val_novo is not None and val_antigo != val_novo:
            setattr(config_atual, attr, val_novo)
            msg = f"[NEAT] {attr}: {val_antigo} -> {val_novo}"
            print(msg)
            logger.info(msg)

    print("✅ Configuração dinâmica aplicada.")
    logger.info("======== FIM DA ATUALIZAÇÃO DINÂMICA ========\n")


def log_genome_config(config, path="genome_config_log.txt"):
    genome_cfg_dict = vars(config.genome_config)
    with open(path, "w", encoding="utf-8") as f:
        f.write("=== GENOME CONFIG ===\n")
        for key, value in genome_cfg_dict.items():
            f.write(f"{key:30} = {value}\n")
