import os

def get_env_var(var):
    return os.environ[var]

# Some global envvars
uploaded_images_dir = get_env_var("ORIG_IMG_DIR")
optimized_images_dir = get_env_var("OPT_IMG_DIR")
async_download_chunk_size = int(get_env_var("DL_CHUNK_SIZE"))
mqtt_host = get_env_var("MQTT_HOST")
process_count = int(get_env_var("PIL_PROCESS_COUNT"))
ingoing_queue_name = "orig_img"
outgoing_queue_name = "opt_img"
