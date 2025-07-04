import React, { useRef, useState } from "react";
import Head from "next/head";
import ReactMarkdown from "react-markdown";

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

export default function Home() {
  const [pdfFiles, setPdfFiles] = useState<File[]>([]);
  const [uploadProgress, setUploadProgress] = useState<number>(0);
  const [uploading, setUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<any>(null);

  const [chatInput, setChatInput] = useState("");
  // Initialize chat with welcome message
  const [chatHistory, setChatHistory] = useState<{ role: string; content: string }[]>([
    {
      role: "assistant",
      content:
        "Hello! I'm ready to answer your questions about the uploaded financial statement. What would you like to know?",
    },
  ]);
  const [aiSources, setAiSources] = useState<any[]>([]);
  const [loadingAnswer, setLoadingAnswer] = useState(false);

  const fileInputRef = useRef<HTMLInputElement>(null);

  // Handle PDF file selection
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      // Append new files to the existing list, avoiding duplicates by name
      const newFiles = Array.from(e.target.files);
      setPdfFiles((prev) => {
        const existingNames = new Set(prev.map((f) => f.name));
        const filteredNew = newFiles.filter((f) => !existingNames.has(f.name));
        return [...prev, ...filteredNew];
      });
      setUploadStatus(null);
      setUploadProgress(0);
    }
  };

  // Handle PDF upload
  const handleUpload = async () => {
    if (!pdfFiles.length) return;
    setUploading(true);
    setUploadStatus(null);
    setUploadProgress(0);

    const formData = new FormData();
    pdfFiles.forEach((file) => {
      formData.append("files", file);
    });

    try {
      const res = await fetch(`${BACKEND_URL}/api/upload`, {
        method: "POST",
        body: formData,
      });
      if (!res.ok) {
        setUploadStatus("Upload failed");
        setUploading(false);
        return;
      }
      const data = await res.json();
      setUploadStatus(data);
      setUploadProgress(100);
      setPdfFiles([]); // Clear the list after upload finishes
    } catch (err) {
      setUploadStatus("Upload failed");
    }
    setUploading(false);
  };

  // Handle chat send
  const handleSend = async () => {
    if (!chatInput.trim()) return;
    setLoadingAnswer(true);
    setAiSources([]);
    // Add user message to chat history
    setChatHistory((prev) => [...prev, { role: "user", content: chatInput }]);
    const currentHistory = [...chatHistory, { role: "user", content: chatInput }];

    try {
      const res = await fetch(`${BACKEND_URL}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          question: chatInput,
          chat_history: currentHistory,
        }),
      });
      if (!res.ok) {
        // Add error as AI message
        setChatHistory((prev) => [
          ...prev,
          { role: "assistant", content: "Sorry, something went wrong." },
        ]);
        setLoadingAnswer(false);
        setChatInput("");
        return;
      }
      const data = await res.json();
      // Add AI answer to chat history
      setChatHistory((prev) => [
        ...prev,
        { role: "assistant", content: data.answer },
      ]);
      setAiSources(data.sources || []);
    } catch (err) {
      setChatHistory((prev) => [
        ...prev,
        { role: "assistant", content: "Sorry, something went wrong." },
      ]);
    }
    setLoadingAnswer(false);
    setChatInput("");
  };

  return (
    <>
      <Head>
        <title>Financial Insights AI</title>
        <meta name="description" content="AI-powered Q&A system for financial documents" />
        <link rel="icon" href="/favicon.ico" />
        <link rel="preconnect" href="https://fonts.gstatic.com/" crossOrigin="" />
        <link
          rel="stylesheet"
          as="style"
          onLoad={(e) => {
            (e.currentTarget as HTMLLinkElement).rel = "stylesheet";
          }}
          href="https://fonts.googleapis.com/css2?display=swap&family=Inter:wght@400;500;700;900&family=Noto+Sans:wght@400;500;700;900"
        />
      </Head>
      <div
        className="relative flex size-full min-h-screen flex-col bg-slate-50 group/design-root overflow-x-hidden"
        style={{ fontFamily: 'Inter, "Noto Sans", sans-serif' }}
      >
        <div className="layout-container flex h-full grow flex-col">
          <header className="flex items-center justify-between whitespace-nowrap border-b border-solid border-b-[#e7edf4] px-10 py-3">
            <div className="flex items-center gap-4 text-[#0d141c]">
              <div className="size-4">
                <svg viewBox="0 0 48 48" fill="none">
                  <path
                    fillRule="evenodd"
                    clipRule="evenodd"
                    d="M24 4H42V17.3333V30.6667H24V44H6V30.6667V17.3333H24V4Z"
                    fill="currentColor"
                  ></path>
                </svg>
              </div>
              <h2 className="text-[#0d141c] text-lg font-bold leading-tight tracking-[-0.015em]">
                Financial Insights AI
              </h2>
            </div>
            <div className="flex flex-1 justify-end gap-8">
              <div className="flex items-center gap-9">
                <a className="text-[#0d141c] text-sm font-medium leading-normal" href="#">
                  Home
                </a>
                <a className="text-[#0d141c] text-sm font-medium leading-normal" href="#">
                  Documents
                </a>
                <a className="text-[#0d141c] text-sm font-medium leading-normal" href="#">
                  Settings
                </a>
              </div>
              <div
                className="bg-center bg-no-repeat aspect-square bg-cover rounded-full size-10"
                style={{
                  backgroundImage:
                    'url("https://lh3.googleusercontent.com/aida-public/AB6AXuBd1p-BVZJVPJH2sbMcRtlP9RUURkcEpv4FyF-lYapAJZEu2BKW7HE0NcZTa3jAMaGty-xKeaLckDDT_RGJgGGq9aAYgI0wO-JmPnbgiFm0fTsOWiDLvQGK0BU1LxxH3lH0EasntLit0G_jEI7t-WK15iTXTedAzJXhp3oE5aVpBtMIDGiDvCt2IyDcSMXPXOhXfDkq-Nd0rDR-d9If7K3TvagAgsaGStMk9CS4bKEw9LuoDcF-zrY6yKrWFeR_cNgNczd3_CK34mB8")',
                }}
              ></div>
            </div>
          </header>
          <div className="px-40 flex flex-1 justify-center py-5">
            <div className="layout-content-container flex flex-col max-w-[960px] flex-1">
              <div className="flex flex-wrap justify-between gap-3 p-4">
                <p className="text-[#0d141c] tracking-light text-[32px] font-bold leading-tight min-w-72">
                  Financial Statement Q&amp;A
                </p>
              </div>
              {/* File Upload */}
              <div className="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3">
                <label className="flex flex-col min-w-40 flex-1">
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept="application/pdf"
                    multiple
                    className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-[#0d141c] focus:outline-0 focus:ring-0 border border-[#cedbe8] bg-slate-50 focus:border-[#cedbe8] h-14 placeholder:text-[#49739c] p-[15px] text-base font-normal leading-normal"
                    placeholder="Upload financial statements (PDF)"
                    onChange={handleFileChange}
                  />
                </label>
                {pdfFiles.length > 0 && (
                  <ul className="mb-2 space-y-2">
                    {pdfFiles.map((file, idx) => (
                      <li
                        key={file.name}
                        className="flex items-center justify-between bg-white border border-[#e7edf4] rounded-lg px-3 py-2 shadow-sm transition hover:shadow-md"
                      >
                        <div className="flex items-center gap-2">
                          {/* File icon */}
                          <svg
                            className="w-5 h-5 text-[#0c7ff2]"
                            fill="none"
                            stroke="currentColor"
                            strokeWidth={2}
                            viewBox="0 0 24 24"
                          >
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              d="M7 7V3a1 1 0 011-1h8a1 1 0 011 1v18a1 1 0 01-1 1H8a1 1 0 01-1-1v-4"
                            />
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              d="M7 17l-4-4m0 0l4-4m-4 4h14"
                            />
                          </svg>
                          <span className="text-[#0d141c] font-medium truncate max-w-[180px]">
                            {file.name}
                          </span>
                        </div>
                        <button
                          type="button"
                          className="ml-2 px-2 py-1 rounded hover:bg-red-100 text-red-600 transition"
                          title="Remove"
                          onClick={() =>
                            setPdfFiles((files) => files.filter((_, i) => i !== idx))
                          }
                        >
                          <svg
                            className="w-4 h-4"
                            fill="none"
                            stroke="currentColor"
                            strokeWidth={2}
                            viewBox="0 0 24 24"
                          >
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              d="M6 18L18 6M6 6l12 12"
                            />
                          </svg>
                        </button>
                      </li>
                    ))}
                  </ul>
                )}
                <button
                  className="min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-12 px-4 bg-[#0c7ff2] text-slate-50 text-base font-medium leading-normal"
                  disabled={!pdfFiles.length || uploading}
                  onClick={handleUpload}
                >
                  {uploading ? "Uploading..." : "Upload"}
                </button>
              </div>
              {/* Upload Progress */}
                {uploading && (
                <div className="flex flex-col gap-3 p-4 items-center">
                  <div className="flex gap-6 justify-between w-full">
                    <p className="text-[#0d141c] text-base font-medium leading-normal">
                      Uploading...
                    </p>
                  </div>
                  {/* Spinner widget */}
                  <div className="flex justify-center items-center my-2">
                    <svg
                      className="animate-spin h-10 w-10 text-[#0c7ff2]"
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                    >
                      <circle
                        className="opacity-25"
                        cx="12"
                        cy="12"
                        r="10"
                        stroke="currentColor"
                        strokeWidth="4"
                      ></circle>
                      <path
                        className="opacity-75"
                        fill="currentColor"
                        d="M4 12a8 8 0 018-8v8z"
                      ></path>
                    </svg>
                  </div>
                </div>
              )}
              {uploadStatus && (
                <div className="flex flex-col gap-3 p-4">
                  <h4 className="text-[#0d141c] text-base font-semibold mb-2">
                    Upload Results
                  </h4>
                  <table className="min-w-full border border-[#e7edf4] rounded-lg overflow-hidden bg-white shadow">
                    <thead className="bg-[#f5f8fa]">
                      <tr>
                        <th className="px-4 py-2 text-left text-xs font-medium text-[#49739c]">
                          File
                        </th>
                        <th className="px-4 py-2 text-left text-xs font-medium text-[#49739c]">
                          Status
                        </th>
                        <th className="px-4 py-2 text-left text-xs font-medium text-[#49739c]">
                          Chunks
                        </th>
                        <th className="px-4 py-2 text-left text-xs font-medium text-[#49739c]">
                          Time (s)
                        </th>
                      </tr>
                    </thead>
                    <tbody>
                      {uploadStatus.results &&
                        uploadStatus.results.map((r: any, idx: number) => (
                          <tr key={r.filename} className="border-t border-[#e7edf4]">
                            <td className="px-4 py-2 text-sm">{r.filename}</td>
                            <td className="px-4 py-2 text-sm">
                              {r.message.includes("success") ? (
                                <span className="inline-flex items-center gap-1 text-green-600">
                                  <svg
                                    className="w-4 h-4"
                                    fill="none"
                                    stroke="currentColor"
                                    strokeWidth={2}
                                    viewBox="0 0 24 24"
                                  >
                                    <path
                                      strokeLinecap="round"
                                      strokeLinejoin="round"
                                      d="M5 13l4 4L19 7"
                                    />
                                  </svg>
                                  {r.message}
                                </span>
                              ) : (
                                <span className="inline-flex items-center gap-1 text-red-600">
                                  <svg
                                    className="w-4 h-4"
                                    fill="none"
                                    stroke="currentColor"
                                    strokeWidth={2}
                                    viewBox="0 0 24 24"
                                  >
                                    <path
                                      strokeLinecap="round"
                                      strokeLinejoin="round"
                                      d="M6 18L18 6M6 6l12 12"
                                    />
                                  </svg>
                                  {r.message}
                                </span>
                              )}
                            </td>
                            <td className="px-4 py-2 text-sm">{r.chunks_count}</td>
                            <td className="px-4 py-2 text-sm">{r.processing_time}</td>
                          </tr>
                        ))}
                    </tbody>
                  </table>
                </div>
              )}
              {/* Chat Section */}
              <h3 className="text-[#0d141c] text-lg font-bold leading-tight tracking-[-0.015em] px-4 pb-2 pt-4">
                Chat
              </h3>
              {/* Chat Bubbles */}
              <div className="flex flex-col gap-2">
                {chatHistory.map((msg, idx) => (
                  <div
                    key={idx}
                    className={`flex items-end gap-3 p-4 ${msg.role === "user" ? "justify-end" : ""}`}
                  >
                    {msg.role === "assistant" && (
                      <div
                        className="bg-center bg-no-repeat aspect-square bg-cover rounded-full w-10 shrink-0"
                        style={{
                          backgroundImage:
                            'url("https://lh3.googleusercontent.com/aida-public/AB6AXuAWHDBfkEesHNPUrKWB4EgPbeWzpTm5EyQS7xmdGTReYVWJRtcTLG98dskZIAV0mwD85HO3kJlS3y6naGmPSbCfCJXfd8V9gNe0OjcLaLBU_qqQ06Mhi7Xb-ItPjlBlHMxXVc8ss2gmVBIlIaH5qmLFz_C-chFDssyET5Y0cvfKPKctRgp-QVApLqYK20lkzFkXdNPQU-e66Lrupf23JGOgfuTmMSu5ydArWDdd-Gu-ReaSDJrIdfChMGeovY_EX98FiRgOE6tHV1hQ")',
                        }}
                      ></div>
                    )}
                    <div
                      className={`flex flex-1 flex-col gap-1 items-${
                        msg.role === "user" ? "end" : "start"
                      }`}
                    >
                      <p className="text-[#49739c] text-[13px] font-normal leading-normal max-w-[360px]">
                        {msg.role === "user" ? "You" : "AI Assistant"}
                      </p>
                        <div
                          className={`text-base font-normal leading-normal max-w-[360px] break-words whitespace-pre-line rounded-lg px-4 py-3 ${
                            msg.role === "user"
                              ? "bg-[#0c7ff2] text-slate-50"
                              : "bg-[#e7edf4] text-[#0d141c]"
                          }`}
                        >
                          <ReactMarkdown>{msg.content}</ReactMarkdown>
                        </div>
                    </div>
                    {msg.role === "user" && (
                      <div
                        className="bg-center bg-no-repeat aspect-square bg-cover rounded-full w-10 shrink-0"
                        style={{
                          backgroundImage:
                            'url("https://lh3.googleusercontent.com/aida-public/AB6AXuBCfZcMtOGhLYq82aoCXu90d5THnX73QRojjkLjkBwBnr12ClN5Ngq6Qynjb1AVP22A8qjUhdFeuy7uPhOo7Cm2qNIRE35OS3vJaFHk51QMOxVabilrhydZDhDBPGhCnlHIuydCypvj8USiDU83593ZuTnO_DgmAl7fL_QEkB3CihLIjvodjd84lDAWzvO_NhmqTbdSrxnC7he4FIwZpp13yVSykjc5yD_DaP2BudNeZx6VaUy9GWOn0PpetsaEqy7BzgK4KcQVWoF1")',
                        }}
                      ></div>
                    )}
                  </div>
                ))}
                {/* Loading spinner for AI answer */}
                {loadingAnswer && (
                  <div className="flex items-end gap-3 p-4">
                    <div
                      className="bg-center bg-no-repeat aspect-square bg-cover rounded-full w-10 shrink-0"
                      style={{
                        backgroundImage:
                          'url("https://lh3.googleusercontent.com/aida-public/AB6AXuAWHDBfkEesHNPUrKWB4EgPbeWzpTm5EyQS7xmdGTReYVWJRtcTLG98dskZIAV0mwD85HO3kJlS3y6naGmPSbCfCJXfd8V9gNe0OjcLaLBU_qqQ06Mhi7Xb-ItPjlBlHMxXVc8ss2gmVBIlIaH5qmLFz_C-chFDssyET5Y0cvfKPKctRgp-QVApLqYK20lkzFkXdNPQU-e66Lrupf23JGOgfuTmMSu5ydArWDdd-Gu-ReaSDJrIdfChMGeovY_EX98FiRgOE6tHV1hQ")',
                      }}
                    ></div>
                    <div className="flex flex-1 flex-col gap-1 items-start">
                      <p className="text-[#49739c] text-[13px] font-normal leading-normal max-w-[360px]">
                        AI Assistant
                      </p>
                      <div className="flex items-center gap-2">
                        <span className="text-base font-normal leading-normal flex max-w-[360px] rounded-lg px-4 py-3 bg-[#e7edf4] text-[#0d141c]">
                          <svg
                            className="animate-spin h-5 w-5 mr-2 text-[#0c7ff2]"
                            xmlns="http://www.w3.org/2000/svg"
                            fill="none"
                            viewBox="0 0 24 24"
                          >
                            <circle
                              className="opacity-25"
                              cx="12"
                              cy="12"
                              r="10"
                              stroke="currentColor"
                              strokeWidth="4"
                            ></circle>
                            <path
                              className="opacity-75"
                              fill="currentColor"
                              d="M4 12a8 8 0 018-8v8z"
                            ></path>
                          </svg>
                          Generating answer...
                        </span>
                      </div>
                    </div>
                  </div>
                )}
              </div>
              {/* Chat Input */}
              <div className="flex items-center px-4 py-3 gap-3 @container">
                <label className="flex flex-col min-w-40 h-12 flex-1">
                  <div className="flex w-full flex-1 items-stretch rounded-lg h-full">
                    <input
                      placeholder="Ask a question..."
                      className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-[#0d141c] focus:outline-0 focus:ring-0 border-none bg-[#e7edf4] focus:border-none h-full placeholder:text-[#49739c] px-4 rounded-r-none border-r-0 pr-2 text-base font-normal leading-normal"
                      value={chatInput}
                      onChange={(e) => setChatInput(e.target.value)}
                      onKeyDown={(e) => {
                        if (e.key === "Enter") handleSend();
                      }}
                      disabled={loadingAnswer}
                    />
                    <div className="flex border-none bg-[#e7edf4] items-center justify-center pr-4 rounded-r-lg border-l-0 !pr-2">
                      <div className="flex items-center gap-4 justify-end">
                        <div className="flex items-center gap-1">
                          <button
                            className="flex items-center justify-center p-1.5"
                            tabIndex={-1}
                            disabled
                          >
                            <div
                              className="text-[#49739c]"
                              data-icon="Paperclip"
                              data-size="20px"
                              data-weight="regular"
                            >
                              <svg
                                xmlns="http://www.w3.org/2000/svg"
                                width="20px"
                                height="20px"
                                fill="currentColor"
                                viewBox="0 0 256 256"
                              >
                                <path d="M209.66,122.34a8,8,0,0,1,0,11.32l-82.05,82a56,56,0,0,1-79.2-79.21L147.67,35.73a40,40,0,1,1,56.61,56.55L105,193A24,24,0,1,1,71,159L154.3,74.38A8,8,0,1,1,165.7,85.6L82.39,170.31a8,8,0,1,0,11.27,11.36L192.93,81A24,24,0,1,0,159,47L59.76,147.68a40,40,0,1,0,56.53,56.62l82.06-82A8,8,0,0,1,209.66,122.34Z"></path>
                              </svg>
                            </div>
                          </button>
                        </div>
                        <button
                          className="min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-8 px-4 bg-[#0c7ff2] text-slate-50 text-sm font-medium leading-normal hidden @[480px]:block"
                          onClick={handleSend}
                          disabled={loadingAnswer || !chatInput.trim()}
                        >
                          <span className="truncate">
                            {loadingAnswer ? "Sending..." : "Send"}
                          </span>
                        </button>
                      </div>
                    </div>
                  </div>
                </label>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
