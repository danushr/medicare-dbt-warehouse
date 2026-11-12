{ config, ... }:
{
  languages.python = {
    enable = true;
    uv.enable = true;
    uv.sync.enable = true;
  };

  env.MEDICARE_PROJECT_DIR = config.devenv.root;
  env.MEDICARE_DATA_DIR = "${config.devenv.root}/data";
  env.DBT_PROJECT_DIR = config.devenv.root;
  env.DBT_PROFILES_DIR = config.devenv.root;
  env.AIRFLOW_HOME = "${config.devenv.root}/.airflow";
  env.AIRFLOW__CORE__DAGS_FOLDER = "${config.devenv.root}/dags";
  env.AIRFLOW__CORE__LOAD_EXAMPLES = "false";
}
