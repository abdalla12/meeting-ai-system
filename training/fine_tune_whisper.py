

import argparse
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_args():
    parser = argparse.ArgumentParser(description="Fine-tune Whisper for meeting transcription")
    parser.add_argument("--model_name", type=str, default="openai/whisper-small", help="Base Whisper model")
    parser.add_argument("--dataset", type=str, default="mozilla-foundation/common_voice_13_0", help="HuggingFace dataset")
    parser.add_argument("--language", type=str, default="ko", help="Target language for fine-tuning")
    parser.add_argument("--output_dir", type=str, default="./whisper-finetuned", help="Output directory")
    parser.add_argument("--num_train_epochs", type=int, default=3)
    parser.add_argument("--per_device_train_batch_size", type=int, default=8)
    parser.add_argument("--learning_rate", type=float, default=1e-5)
    parser.add_argument("--warmup_steps", type=int, default=500)
    parser.add_argument("--max_steps", type=int, default=-1)
    parser.add_argument("--fp16", action="store_true", help="Use FP16 training")
    return parser.parse_args()

def main():
    args = parse_args()
    logger.info(f"Fine-tuning Whisper: {args.model_name}")
    logger.info(f"Dataset: {args.dataset}, Language: {args.language}")

    try:
        from transformers import (
            WhisperForConditionalGeneration,
            WhisperProcessor,
            WhisperTokenizer,
            WhisperFeatureExtractor,
            Seq2SeqTrainer,
            Seq2SeqTrainingArguments,
        )
        from datasets import load_dataset, Audio
        import torch
    except ImportError as e:
        logger.error(f"Missing dependency: {e}")
        logger.error("Install: pip install transformers datasets torch torchaudio")
        return

    logger.info("Loading model and processor...")
    processor = WhisperProcessor.from_pretrained(args.model_name)
    model = WhisperForConditionalGeneration.from_pretrained(args.model_name)
    tokenizer = WhisperTokenizer.from_pretrained(args.model_name, language=args.language, task="transcribe")
    feature_extractor = WhisperFeatureExtractor.from_pretrained(args.model_name)

    model.config.forced_decoder_ids = None
    model.config.suppress_tokens = []

    logger.info(f"Loading dataset: {args.dataset}")
    dataset = load_dataset(args.dataset, args.language, split="train[:1000]", trust_remote_code=True)
    dataset = dataset.cast_column("audio", Audio(sampling_rate=16000))

    def prepare_dataset(batch):
        audio = batch["audio"]
        batch["input_features"] = feature_extractor(
            audio["array"], sampling_rate=audio["sampling_rate"]
        ).input_features[0]
        batch["labels"] = tokenizer(batch["sentence"]).input_ids
        return batch

    logger.info("Preprocessing dataset...")
    dataset = dataset.map(prepare_dataset, remove_columns=dataset.column_names)

    training_args = Seq2SeqTrainingArguments(
        output_dir=args.output_dir,
        per_device_train_batch_size=args.per_device_train_batch_size,
        learning_rate=args.learning_rate,
        warmup_steps=args.warmup_steps,
        max_steps=args.max_steps if args.max_steps > 0 else None,
        num_train_epochs=args.num_train_epochs,
        fp16=args.fp16,
        evaluation_strategy="no",
        save_strategy="epoch",
        logging_steps=25,
        report_to="none",
        predict_with_generate=True,
        generation_max_length=225,
    )

    trainer = Seq2SeqTrainer(
        args=training_args,
        model=model,
        train_dataset=dataset,
        tokenizer=processor.feature_extractor,
    )

    logger.info("Starting training...")
    trainer.train()

    logger.info(f"Saving model to {args.output_dir}")
    trainer.save_model(args.output_dir)
    processor.save_pretrained(args.output_dir)

    logger.info("Fine-tuning complete!")

if __name__ == "__main__":
    main()
