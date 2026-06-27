import { useState, useEffect } from "react";
import api from "./services/api";

export default function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [confidence, setConfidence] = useState(0);
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);
  const [file, setFile] = useState(null);
  const [uploadMessage, setUploadMessage] = useState("");
  const [uploadedDocuments, setUploadedDocuments] = useState([]);
 const [uploading, setUploading] = useState(false);

  useEffect(() => { loadDocuments();}, []);

  const askQuestion = async () => {
    console.log("Button clicked"); 
    if (!question.trim()) return;
    try {
      setLoading(true);

      const response = await api.post(
        "/api/chat/query",
        {
          question,
          top_k: 5,
        }
      );

      setAnswer(response.data.answer);
      setConfidence(
        Math.round(
          (response.data.confidence || 0) * 100
        )
      );

      setSources(response.data.sources || []);
    } catch (error) {
      console.error(error);

      setAnswer(
        "Failed to retrieve answer from server."
      );
    } finally {
      setLoading(false);
    }
  };

  const loadDocuments = async () => {
    const response = await api.get(
      "/api/documents"
    );
    console.log(response.data);
    setUploadedDocuments(
      response.data.documents
    );
  };

  const uploadDocument = async () => {
  if (!file) {
    setUploadMessage("Please select a file.");
    return;
  }

  try {
    setUploading(true);
    const formData = new FormData();

    formData.append("file", file);

    const response = await api.post(
      "/api/documents/upload",
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }
    );

    setUploadMessage(
      response.data.message
    );

    if (response.data.status === "Uploaded") {
      await loadDocuments();
    }
  } catch (error) {
    console.error(error);
    setUploadMessage("Document upload failed.");
  } finally {
    setUploading(false);
  }
};

return (
  <div className="h-screen bg-slate-100 flex flex-col">

    {/* ================= HEADER ================= */}

    <header className="h-16 bg-slate-900 text-white flex items-center justify-between px-6 shadow-lg">

      <div>

        <h1 className="text-xl font-bold">
          Enterprise Knowledge Assistant
        </h1>

        <p className="text-xs text-slate-300">
          AI-Powered Enterprise Document Search
        </p>

      </div>

      <div className="text-sm text-green-400">

        ● Connected

      </div>

    </header>

    {/* ================= BODY ================= */}

    <div className="flex flex-1 overflow-hidden">

      {/* ================= LEFT SIDEBAR ================= */}

      <aside className="w-80 bg-white border-r border-slate-200 flex flex-col">

        {/* Upload */}

        <div className="p-5 border-b border-slate-200">

          <h2 className="text-lg font-semibold mb-4">

            📤 Upload Document

          </h2>

          <input
            type="file"
            onChange={(e) => setFile(e.target.files[0])}
            className="w-full text-sm border rounded-lg p-2"
          />

          {file && (

            <div className="mt-3 text-xs text-green-600 truncate">

              Selected: {file.name}

            </div>

          )}

          <button
            onClick={uploadDocument}
            disabled={uploading}
            className="mt-4 w-full bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white rounded-lg py-2"
          >

            {uploading
              ? "Uploading..."
              : "Upload"}

          </button>

          {uploadMessage && (

            <div className="mt-3 text-xs text-slate-600">

              {uploadMessage}

            </div>

          )}

        </div>

        {/* Documents */}

        <div className="flex-1 overflow-hidden">

          <div className="p-5 border-b border-slate-200">

            <div className="flex justify-between items-center">

              <h2 className="font-semibold">

                📚 Knowledge Base

              </h2>

              <span className="text-xs bg-slate-200 rounded-full px-2 py-1">

                {uploadedDocuments.length}

              </span>

            </div>

          </div>

          <div className="overflow-y-auto h-full p-3">

            {uploadedDocuments.length === 0 ? (

              <div className="text-sm text-slate-500 mt-5">

                No documents uploaded

              </div>

            ) : (

              uploadedDocuments.map((doc, index) => (

                <div
                  key={index}
                  className="flex items-center gap-2 border rounded-lg px-3 py-2 mb-2 hover:bg-slate-50 cursor-pointer transition"
                >

                  <span>

                    📄

                  </span>

                  <span className="text-sm truncate">

                    {doc.document_name}

                  </span>

                </div>

              ))

            )}

          </div>

        </div>

      </aside>

      {/* ================= MAIN CONTENT ================= */}

      <main className="flex-1 flex flex-col bg-slate-50">

        {/* Answer Area */}

        <div className="flex-1 overflow-y-auto px-10 py-8">

          <div className="max-w-6xl mx-auto h-full">

            <div className="bg-white rounded-2xl shadow-lg p-10 min-h-full">

              <div className="flex items-center gap-3 mb-6">

                <div className="h-12 w-12 rounded-full bg-blue-600 text-white flex items-center justify-center text-xl">

                  🤖

                </div>

                <div>

                  <h2 className="font-bold text-lg">

                    Enterprise Knowledge Assistant

                  </h2>

                  <p className="text-sm text-slate-500">

                    Powered by Azure OpenAI + RAG

                  </p>

                </div>

              </div>

              {/* PART 2 STARTS HERE */}

                            {/* Empty State */}

              {!answer && (

                <div className="flex flex-col items-center justify-center py-28">

                  <div className="text-7xl mb-6">

                    🤖

                  </div>

                  <h2 className="text-2xl font-bold text-slate-700">

                    Ask anything about your documents

                  </h2>

                  <p className="mt-3 text-slate-500">

                    Upload enterprise documents and ask questions in natural language.

                  </p>

                </div>

              )}

              {/* AI Response */}

              {answer && (

                <>

                  <div className="whitespace-pre-wrap text-slate-700 text-[17px] leading-9">

                    {answer}

                  </div>

                  {/* Confidence */}

                <div className="mt-10 border-t pt-6">

                    <div className="flex justify-between items-center mb-3">

                        <div className="flex items-center gap-2">

                            <span className="text-lg">

                                {confidence >= 85
                                    ? "🟢"
                                    : confidence >= 60
                                    ? "🟡"
                                    : "🔴"}

                            </span>

                            <span className="font-semibold">

                                {confidence >= 85
                                    ? "High Confidence"
                                    : confidence >= 60
                                    ? "Medium Confidence"
                                    : "Low Confidence"}

                            </span>

                        </div>

                        <span className="font-semibold text-slate-700">

                            {confidence}%

                        </span>

                    </div>

                    <div className="w-full h-2 bg-slate-200 rounded-full">

                        <div
                            className={`h-2 rounded-full ${
                                confidence >= 85
                                    ? "bg-green-600"
                                    : confidence >= 60
                                    ? "bg-yellow-500"
                                    : "bg-red-500"
                            }`}
                            style={{
                                width: `${confidence}%`,
                            }}
                        />

                    </div>

                </div>

                  {/* Sources */}

                  <div className="mt-10">

                    <h3 className="font-semibold text-lg mb-4">

                      Sources ({sources.length})

                    </h3>

                    {sources.length === 0 ? (

                      <div className="text-slate-500">

                        No sources found.

                      </div>

                    ) : (

                      <div className="flex flex-wrap gap-3">

                        {sources.map((source, index) => (

                      <div key={index} className="rounded-full border bg-slate-50 px-4 py-2 hover:bg-slate-100 transition">
                          <div className="text-sm font-medium truncate max-w-[250px]">

                              📄 {source.document_name}

                          </div>
                          <div className="text-xs text-slate-500">

                              Chunk #{source.chunk_index}

                          </div>
                      </div>
                        ))}
                      </div>
                    )}

                  </div>

                </>

              )}

            </div>

          </div>

        </div>

        {/* Bottom Ask Bar */}

        <div className="border-t bg-white px-8 py-5 shadow-inner">

<div className="max-w-5xl mx-auto flex gap-3">

    <textarea
        rows="2"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask anything about your enterprise knowledge..."
        className="flex-1 resize-none rounded-2xl border border-slate-300 bg-slate-50 px-5 py-4 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
    />

    <button
        onClick={askQuestion}
        disabled={loading}
        className="px-8 rounded-2xl bg-blue-600 hover:bg-blue-700 disabled:bg-slate-400 text-white font-semibold transition-all shadow-md"
    >
        {loading ? "Searching..." : "Ask"}
    </button>

    <button
        onClick={() => setQuestion("")}
        disabled={loading || !question.trim()}
        className="px-6 rounded-2xl border border-slate-300 bg-white hover:bg-slate-100 disabled:opacity-50 disabled:cursor-not-allowed font-medium transition-all"
    >
        Clear
    </button>

</div>

        </div>

      </main>

    </div>

  </div>
);
}
 