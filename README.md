# Studyflash Learning API: Multiple-Choice Question Generation (Technical Challenge)

This repository contains a **proof-of-concept backend** for generating multiple-choice questions from document data processed by the Studyflash Learning API. The API ingests user-uploaded documents, segments them into chunks, and identifies topics and summaries. Building on this “chunk” output, this prototype creates quiz-like questions with a single correct answer and three distractors.

---

## Overview

**What the API Does:**
1. **Text Extraction & Chunking** – Takes a PDF or similar document and splits it into manageable chunks.
2. **Topic & Summary Assignment** – Each chunk is annotated with relevant topics and a short summary.
3. **Question Generation (New Feature!)** – Produces multiple-choice questions for each document using the existing chunk data, ensuring each question has:
   - One correct answer
   - Three distractors (plausible but incorrect options)

This approach addresses a popular request: the ability to turn uploaded documents into **exam-like quizzes** for more interactive study materials.

---

## Challenge Objective

1. **Prototype Pipeline**  
   Develop and demonstrate a pipeline that generates **multiple-choice questions** from the chunk data.  

2. **Output Format**  
   - Each generated question should come with:
     - **One correct answer**
     - **Three distractors**  

3. **Extended Thinking**  
   Contemplate how the **Learning API data structure** (currently “chunks” + a single document summary) might be redesigned for better context, flexibility, and richer question generation.

---

## Data

### Inputs

1. **Chunk Objects**  
   - Identified by `"type": "chunk"`.
   - Each chunk includes raw text, a summary, a main topic, and a list of subtopics.

2. **Document Summary**  
   - Identified by `"type": "document_summary"`.
   - Contains an overall summary of the document under `content` and a list of main topics in `main_topics`.

### Outputs

- **Multiple-Choice Questions**  
  For each chunk (or group of chunks), the system generates:
  1. Question Text  
  2. Correct Answer  
  3. Three Distractors  

These questions collectively form a quiz that covers the entire document.

## Additional Consideration: Redesigning the Data Structure

A key reflection point for this project is how documents are initially structured in the Learning API. Currently, documents are represented as a series of “chunks” plus a single summary. While this flat structure works for straightforward flashcard generation, it can limit context for more advanced tasks—like generating complex questions or summaries that span multiple sections. A possible redesign would store documents in a *hierarchical* format that mirrors their real-world organization (sections, subsections, paragraphs). Each level would include its own text, summary, and metadata, preserving important relationships between concepts. This would make it easier to generate context-aware questions, produce multi-layered summaries, and offer fine-grained control over how information is organized, searched, and studied.



