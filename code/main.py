from distutils.debug import DEBUG
import logging
import pandas as pd
from transformers import pipeline, AutoModelForTokenClassification, AutoTokenizer
import glob
from utils import configure_logger,mask_private_info
import sys
import os


parent_dir = os.path.abspath(os.pardir)

# configure logger
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
      logger.error("0 files found please add your csv or xlsx files under input_files directory")
      return "0 files found please add your csv or xlsx files under input_files directory"

    logger.info(f"{len(files)} found files in input files")

    for i in files:
      ################################
      #      read file               #
      ################################
      filename = i.split("/")[-1]
      if ".csv" in i.split("/")[-1]:
          #read file
          try:
            df = pd.read_csv(i)
          except Exception as e:
            logger.error(f"Unable to read this file {filename}, your file structure might be corrupt")
            continue
      else:
        logger.error("Your files should a csv file")
        continue

      if data_col not in df.columns:
        logger.error("Data column not found")
        return "Data column not found"


      logger.info(f"Processing {len(df)} lines in the file {filename} started....")
      new_texts = []
      ################################
      #     Mask User info Section   #
      ################################
      masked_lines_counter = 0
      processed_lines = 0
      for text in df[data_col]:
        #process text
        masked_text = mask_private_info(text,ner)
        new_texts.append(masked_text)
        #check if any info was masked
        if "*****" in masked_text:
          masked_lines_counter += 1
        processed_lines += 1
        if processed_lines % 1000 == 0:
          logger.info(f"{masked_lines_counter}/{processed_lines} were masked")


      df["Masked"] = new_texts
      #drop original column
      df = df.drop([data_col],axis=1)
      #save new file
      df.to_csv(os.path.join(parent_dir,"output_files/"+filename))
      logger.info(f"Checking {filename} finished with {masked_lines_counter}/{processed_lines} lines masked")
  except Exception as e:
    logger.error(f"Main function failed with error {e}")
    return f"Main function failed with error {e}"

main()