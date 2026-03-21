import os
from loguru import logger
import config


def list_folders(directory):
    list = []
    for name in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, name)):
            list.append(name)
    return list


def open_the_only_file(directory):
    # open the only poc file of the directory
    files_and_dirs = os.listdir(directory)

    files = [
        file for file in files_and_dirs if os.path.isfile(os.path.join(directory, file))
    ]

    if files:
        first_file_path = os.path.join(directory, files[0])
        with open(first_file_path, "r") as file:
            return file.read()
    else:
        logger.warning("poc not found: " + directory)
        return "error"

'''
def eval_llm(model, model_type):
    count_all = 0
    count_err = 0
    languages = list_folders("dataset/")
    for language in languages:
        cve_list = list_folders(os.path.join("dataset/", language))
        # handle each cv
        for cve in cve_list:
            logger.info("Handle: " + cve)
            for exp in ["1", "2", "3"]:
                # 实验轮数
                for repeat in range(0, 1):
                    save_dir = os.path.join(
                        "./result", config.mode, model_type, language, exp
                    )
                    target = os.path.join(save_dir, str(repeat) + "-" + cve + ".rb")
                    if os.path.exists(target):
                        logger.info(target + " exist!")
                        continue

                    poc = open_the_only_file(
                        os.path.join("dataset/", language, cve, exp)
                    )
                    count_all = count_all + 1
                    if poc != "error":
                        try:
                            # very ugly and refactor is needed
                            if model_type == "codet5p":
                                model_output = model.run_model(
                                    config.user_prompt(language), poc
                                )
                            else:
                                model_output = model.run_model(
                                    config.user_prompt(language) + poc
                                )
                            if not os.path.exists(save_dir):
                                os.makedirs(save_dir)
                            with open(target, "w") as f:
                                f.write(model_output)
                                logger.info("Done: " + target)
                                continue
                        except Exception as e:
                            logger.error(save_dir + " " + str(e))
                    count_err = count_err + 1
    logger.info(
        "{} is finished, total {} with {} error.".format(
            model_type, count_all, count_err
        )
    )
'''
def eval_llm(model, model_type):
    count_all = 0
    count_err = 0
    languages = list_folders("dataset/")
    for language in languages:
        cve_list = list_folders(os.path.join("dataset/", language))
        # handle each cve
        for cve in cve_list:
            logger.info("Handle: " + cve)
            # 只使用 dataset/{language}/{cve}/3/ 作为输入
            exp = "3"  # 固定使用 exp = "3"
            # 进行三次重复实验
            for repeat in range(1, 4):  # 重复 3 次，轮数从 1 开始
                save_dir = os.path.join(
                    "./result", config.mode, f"{model_type}_{repeat}", language
                )
                # 输出文件名为 cve-xxx-xxx.txt
                target = os.path.join(save_dir, f"{cve}.txt")
                if os.path.exists(target):
                    logger.info(target + " exist!")
                    continue

                poc = open_the_only_file(
                    os.path.join("dataset/", language, cve, exp)
                )
                count_all = count_all + 1
                if poc != "error":
                    try:
                        # very ugly and refactor is needed
                        if model_type == "codet5p":
                            model_output = model.run_model(
                                config.user_prompt(language), poc
                            )
                        else:
                            model_output = model.run_model(
                                config.user_prompt(language) + poc
                            )
                        if not os.path.exists(save_dir):
                            os.makedirs(save_dir)
                        with open(target, "w") as f:
                            f.write(model_output)
                            logger.info("Done: " + target)
                            continue
                    except Exception as e:
                        logger.error(save_dir + " " + str(e))
                count_err = count_err + 1
    logger.info(
        "{} is finished, total {} with {} error.".format(
            model_type, count_all, count_err
        )
    )

