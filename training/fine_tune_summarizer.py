

import argparse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_args():
    parser = argparse.ArgumentParser(description="Fine-tune T5 for meeting summarization")
    parser.add_argument("--model_name", type=str, default="google/flan-t5-base")
    parser.add_argument("--dataset", type=str, default="samsum", help="Summarization dataset")
    parser.add_argument("--output_dir", type=str, default="./t5-meeting-summarizer")
    parser.add_argument("--num_train_epochs", type=int, default=3)
    parser.add_argument("--per_device_train_batch_size", type=int, default=4)
    parser.add_argument("--learning_rate", type=float, default=3e-5)
    parser.add_argument("--max_input_length", type=int, default=1024)
    parser.add_argument("--max_target_length", type=int, default=256)
    parser.add_argument("--fp16", action="store_true")
    return parser.parse_args()

def main():
    args = parse_args()
    logger.info(f"Fine-tuning T5: {args.model_name}")

    try:
        from transformers import (
            T5ForConditionalGeneration,
            T5Tokenizer,
            Seq2SeqTrainer,
            Seq2SeqTrainingArguments,
            DataCollatorForSeq2Seq,
        )
        from datasets import load_dataset
    except ImportError as e:
        logger.error(f"Missing dependency: {e}")
        logger.error("Install: pip install transformers datasets torch")
        return

    logger.info("Loading model and tokenizer...")
    tokenizer = T5Tokenizer.from_pretrained(args.model_name)
    model = T5ForConditionalGeneration.from_pretrained(args.model_name)

    logger.info(f"Loading dataset: {args.dataset}")
    dataset = load_dataset(args.dataset)

    def preprocess(examples):

        inputs = [f"summarize the following meeting:\n{d}" for d in examples["dialogue"]]
        targets = examples["summary"]

        model_inputs = tokenizer(
            inputs, max_length=args.max_input_length, truncation=True, padding="max_length"
        )
        labels = tokenizer(
            targets, max_length=args.max_target_length, truncation=True, padding="max_length"
        )

        model_inputs["labels"] = labels["input_ids"]
        return model_inputs

    logger.info("Preprocessing dataset...")
    tokenized = dataset.map(preprocess, batched=True, remove_columns=dataset["train"].column_names)

    data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

    training_args = Seq2SeqTrainingArguments(
        output_dir=args.output_dir,
        num_train_epochs=args.num_train_epochs,
        per_device_train_batch_size=args.per_device_train_batch_size,
        learning_rate=args.learning_rate,
        fp16=args.fp16,
        save_strategy="epoch",
        logging_steps=50,
        report_to="none",
        predict_with_generate=True,
    )

    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=tokenized["train"],
        eval_dataset=tokenized.get("validation"),
        tokenizer=tokenizer,
        data_collator=data_collator,
    )

    logger.info("Starting training...")
    trainer.train()

    logger.info(f"Saving model to {args.output_dir}")
    trainer.save_model(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)

    logger.info("Fine-tuning complete!")

if __name__ == "__main__":
    main()
