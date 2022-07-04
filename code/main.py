from distutils.debug import DEBUG
import logging
import pandas as pd
from transformers import pipeline, AutoModelForTokenClassification, AutoTokenizer
import glob
from utils import configure_logger,mask_private_info
import sys
import os
from tqdm import tqdm



parent_dir = os.path.abspath(os.pardir)

# configure #logger
logger = configure_logger(
    logging,
    # log file name
    os.path.join(parent_dir,"logs/pivony_masking.log"),
    # file logging level
    DEBUG,
)

################################
#      Model Import            #
################################
tokenizer = AutoTokenizer.from_pretrained("savasy/bert-base-turkish-ner-cased")
model = AutoModelForTokenClassification.from_pretrained("savasy/bert-base-turkish-ner-cased")
ner=pipeline('ner', model=model, tokenizer=tokenizer)


def main():
  try:
    data_col = "Verbatim"
    #read all files in input_files
    files = glob.glob(os.path.join(parent_dir,"input_files/*"))
    if len(files) == 0:
      print("0 files found please add your csv files under input_files directory")
      logger.error("0 files found please add your csv files under input_files directory")
      return "0 files found please add your csv files under input_files directory"

    logger.info(f"{len(files)} found files in input files")
    print(f"{len(files)} found files in input files")

    for file in files:
      ################################
      #      read file               #
      ################################
      if "/" in i:
        filename = i.split("/")[-1]
      else:
        filename = i.split("\\")[-1]

      logger.info(f"reading file {filename} started")
      print(f"reading file {filename} started")
      if ".csv" in filename:
          #read file
          try:
            df = pd.read_csv(file)
            read_csv_success = True
          except Exception as e:
            read_csv_success = False
          if read_csv_success is False:
            #read csv in a diffrent turkish supporting encoding
            tr_char_encoding = ["cp1026", "iso8859_9", "mac_turkish", "cp857", "cp1254", "cp857"]
            reading_encoding = False
            for encoding in tr_char_encoding:
              try:
                logger.info(f"encoding with {encoding} started")
                df = pd.read_csv(file, encoding=encoding)
                logger.info(f"encoding with {encoding} succeeded")
                reading_encoding = True
                break
              except Exception as e:
                logger.error(e)
                logger.error(f"encoding with {encoding} failed")

            if reading_encoding is False:
              print(f"Unable to read this file {filename}, your file structure might be corrupt")
              logger.error(f"Unable to read this file {filename}, your file structure might be corrupt")
              continue
      else:
        print("Your files should be in csv : comma seperated format")
        continue
      print("we are out of reading")
      if data_col not in df.columns:
        print("Data column not found")
        return "Data column not found"


      print(f"Processing {len(df)} lines in the file {filename} started....")
      new_texts = []
      ################################
      #     Mask User info Section   #
      ################################
      masked_lines_counter = 0
      processed_lines = 0
      texts = df[data_col]
      for text_index in tqdm(range(len(df))):
        #process text
        masked_text = mask_private_info(texts[text_index],ner)
        new_texts.append(masked_text)
        #check if any info was masked
        if "*****" in masked_text:
          masked_lines_counter += 1
        processed_lines += 1
        if processed_lines % 10 == 0:
          print(f"{masked_lines_counter}/{processed_lines} were masked")
          logger.info(f"{masked_lines_counter}/{processed_lines} were masked")

      df["Masked"] = new_texts
      #drop original column
      df = df.drop([data_col],axis=1)
      #save new file
      df.to_csv(os.path.join(parent_dir,"output_files/"+filename),index=False,encoding="utf-8-sig")
      print(f"Checking {filename} finished with {masked_lines_counter}/{processed_lines} lines masked")
      logger.info(f"Checking {filename} finished with {masked_lines_counter}/{processed_lines} lines masked")
  except Exception as e:
    print(f"Main function failed with error {e}")
    return e

main()