# Резюме главы 9

Source section: explicit «Резюме» in `p0269:c01`.

The chapter argues that a growing RAG system eventually contains two broad categories of data:

- dynamic information that changes frequently and remains suitable for retrieval;
- stable/static information that may remain unchanged for long periods and can become a candidate for fine-tuning.

The worked example reuses the SciQ science dataset from the previous chapter.

The source:
1. downloads and filters SciQ;
2. separates questions, correct answers and explanations;
3. converts them into chat-style prompt/answer examples;
4. writes a JSONL-style training file;
5. uploads the file to OpenAI;
6. starts fine-tuning of GPT-4o-mini;
7. monitors training jobs and errors;
8. retrieves the resulting fine-tuned model identifier;
9. tests the model with a known science question;
10. inspects OpenAI training metrics and usage information.

Human feedback remains part of the conceptual pipeline because the quality of the training data determines the value of fine-tuning.

The chapter concludes that fine-tuning can reduce RAG-management overhead for suitable stable data, but does not claim that every RAG corpus should be converted into model parameters.

Chapter 10 returns to a larger RAG ecosystem with video generation, Pinecone and OpenAI.

## Provenance

- Summary source: `p0269:c01`
- Cross-check: `p0253:c01–p0268:c01`
