# Резюме главы 6

Source section: explicit chapter-end «Резюме» in `p0197:c01`.

The chapter builds a scaled RAG recommendation system intended to reduce bank customer churn.

The workflow contains three components.

1. **Data collection and preparation**
   - download Bank Customer Churn data from Kaggle;
   - remove selected unnecessary/sensitive fields for the scenario;
   - perform exploratory analysis;
   - identify the strong complaint/churn pattern described by the source;
   - evaluate k-means cluster configurations.

2. **Pinecone index scaling**
   - convert customer rows into text chunks;
   - generate embeddings with OpenAI;
   - simulate larger vector counts by duplicating chunks/embeddings;
   - create a Pinecone serverless index;
   - upload records in batches using upsert;
   - inspect vector counts and query performance.

3. **RAG generation**
   - create a target customer profile;
   - retrieve similar customer vectors from Pinecone;
   - combine retrieved metadata with the target profile;
   - send the augmented prompt to GPT-4o;
   - generate a personalized retention email.

The source repeatedly emphasizes that scaling requires active management of:
- model/API limits;
- embedding and generation cost;
- vector-store read/write/storage cost;
- cloud/region selection;
- latency;
- batch size;
- data volume.

The chapter concludes that a target-vector approach can support personalized recommendations and points toward a richer knowledge-oriented system in the next chapter.

## Provenance

- Summary source: `p0197:c01`
- Context cross-check: `p0161:c01–p0196:c01`
