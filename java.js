import React, { useState } from 'react';

const AppCompilerUI = () => {
  const [prompt, setPrompt] = useState("");
  const [config, setConfig] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleCompile = async () => {
    setLoading(true);
    const response = await fetch("http://localhost:8000/compile", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt }),
    });
    const data = await response.json();
    setConfig(data);
    setLoading(false);
  };

  const renderComponent = (comp) => {
    switch (comp.component_type) {
      case 'DataTable':
        return (
          <div className="p-5 border border-white/10 rounded-2xl bg-slate-900/50 backdrop-blur-md shadow-xl transition-all hover:scale-[1.02] hover:border-indigo-500/50 duration-300">
            <h4 className="font-bold text-white mb-3">{comp.label}</h4>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm text-slate-300 border-collapse">
                <thead>
                  <tr className="bg-white/5 border-b border-white/5 text-xs uppercase tracking-wider text-slate-400">
                    <th className="p-3">ID</th>
                    <th className="p-3">Name</th>
                    <th className="p-3">Status</th>
                  </tr>
                </thead>
                <tbody>
                  <tr className="border-b border-white/5 hover:bg-white/5 transition-colors">
                    <td className="p-3 text-slate-400 font-mono text-xs">01</td>
                    <td className="p-3 font-medium text-white">Sample Item 1</td>
                    <td className="p-3"><span className="px-2 py-1 rounded text-[10px] bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">Active</span></td>
                  </tr>
                  <tr className="hover:bg-white/5 transition-colors">
                    <td className="p-3 text-slate-400 font-mono text-xs">02</td>
                    <td className="p-3 font-medium text-white">Sample Item 2</td>
                    <td className="p-3"><span className="px-2 py-1 rounded text-[10px] bg-slate-500/10 text-slate-400 border border-slate-500/20">Inactive</span></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        );
      case 'Form':
        return (
          <div className="p-5 border border-white/10 rounded-2xl bg-slate-900/50 backdrop-blur-md shadow-xl transition-all hover:scale-[1.02] hover:border-indigo-500/50 duration-300">
            <h4 className="font-bold text-white mb-3">{comp.label}</h4>
            <form className="space-y-3" onSubmit={(e) => e.preventDefault()}>
              <input type="text" placeholder="Name" className="w-full bg-slate-900/60 border border-white/10 text-white p-3 rounded-xl text-sm focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-colors placeholder-slate-500" />
              <input type="email" placeholder="Email" className="w-full bg-slate-900/60 border border-white/10 text-white p-3 rounded-xl text-sm focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-colors placeholder-slate-500" />
              <textarea placeholder="Message" className="w-full bg-slate-900/60 border border-white/10 text-white p-3 rounded-xl text-sm focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-colors placeholder-slate-500 h-24 resize-none"></textarea>
              <button type="submit" className="w-full bg-indigo-600 hover:bg-indigo-500 text-white py-3 rounded-xl text-sm font-semibold transition-colors shadow-lg shadow-indigo-500/20">Submit</button>
            </form>
          </div>
        );
      case 'Chart':
        return (
          <div className="p-5 border border-white/10 rounded-2xl bg-slate-900/50 backdrop-blur-md shadow-xl transition-all hover:scale-[1.02] hover:border-indigo-500/50 duration-300">
            <h4 className="font-bold text-white mb-3">{comp.label}</h4>
            <div className="h-40 rounded-xl bg-slate-900/50 border border-white/5 flex flex-col items-center justify-center relative overflow-hidden group">
                <div className="absolute bottom-0 w-full flex items-end justify-around px-4 h-24 opacity-70 group-hover:opacity-100 transition-opacity">
                    <div className="w-8 bg-indigo-500/80 rounded-t-sm h-12"></div>
                    <div className="w-8 bg-purple-500/80 rounded-t-sm h-20"></div>
                    <div className="w-8 bg-indigo-400/80 rounded-t-sm h-16"></div>
                    <div className="w-8 bg-purple-400/80 rounded-t-sm h-8"></div>
                </div>
                <span className="text-xs text-slate-500 font-medium z-10 bg-slate-900/80 px-3 py-1 rounded-full border border-white/5">Chart Visualization</span>
            </div>
          </div>
        );
      case 'Card':
        return (
          <div className="p-5 border border-white/10 rounded-2xl bg-gradient-to-br from-indigo-500/10 to-purple-500/10 backdrop-blur-md shadow-xl transition-all hover:scale-[1.02] hover:border-indigo-500/50 duration-300">
            <h4 className="font-bold text-white mb-2">{comp.label}</h4>
            <p className="text-slate-400 text-sm">This is an interactive card component displaying key metrics or information.</p>
            <div className="mt-4 text-2xl font-bold text-white">8,492</div>
            <div className="text-xs text-emerald-400 mt-1">+24% from last week</div>
          </div>
        );
      case 'Navbar':
        return (
          <nav className="p-5 border border-white/10 rounded-2xl bg-slate-900/50 backdrop-blur-md shadow-xl transition-all hover:scale-[1.02] hover:border-indigo-500/50 duration-300">
            <h4 className="font-bold text-white mb-3">{comp.label}</h4>
            <div className="flex flex-wrap gap-2 text-sm mt-2">
              <a href="#" className="px-3 py-1.5 rounded-lg bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 hover:bg-indigo-500/30 transition-colors">Home</a>
              <a href="#" className="px-3 py-1.5 rounded-lg bg-white/5 text-slate-400 border border-white/5 hover:bg-white/10 hover:text-white transition-colors">About</a>
              <a href="#" className="px-3 py-1.5 rounded-lg bg-white/5 text-slate-400 border border-white/5 hover:bg-white/10 hover:text-white transition-colors">Contact</a>
            </div>
          </nav>
        );
      default:
        return (
          <div className="p-5 border border-white/10 rounded-2xl bg-slate-900/50 backdrop-blur-md shadow-xl transition-all hover:scale-[1.02] hover:border-indigo-500/50 duration-300">
            <div className="flex items-center gap-2 mb-2">
                <span className="text-[10px] font-bold uppercase tracking-widest text-indigo-300 bg-indigo-500/10 border border-indigo-500/20 px-2 py-0.5 rounded-full">{comp.component_type}</span>
            </div>
            <h4 className="font-bold text-white mb-2">{comp.label}</h4>
            <div className="text-[11px] text-slate-400 font-mono bg-slate-900/50 p-2 rounded border border-white/5 truncate">API: {comp.data_source}</div>
          </div>
        );
    }
  };
  

  return (
    <div className="flex h-screen bg-slate-950 font-sans text-slate-200 relative overflow-hidden">
      {/* Background Effects */}
      <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] rounded-full bg-indigo-600/10 blur-[120px] pointer-events-none"></div>
      <div className="absolute bottom-[-20%] right-[-10%] w-[50%] h-[50%] rounded-full bg-purple-600/10 blur-[120px] pointer-events-none"></div>

      {/* LEFT: Compiler Input */}
      <div className="w-1/3 p-8 bg-slate-900/40 backdrop-blur-xl border-r border-white/5 flex flex-col z-10 shadow-2xl">
        <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shadow-lg shadow-indigo-500/30">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
            </div>
            <h2 className="text-2xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-purple-400">AI Compiler</h2>
        </div>
        <textarea 
          className="flex-1 p-5 bg-slate-900/60 border border-white/10 rounded-2xl shadow-inner text-white focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-colors placeholder-slate-500 resize-none"
          placeholder="Describe the application you want to build (e.g. A CRM for real estate agents)..."
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
        />
        <button 
          onClick={handleCompile}
          disabled={loading}
          className={`mt-6 py-4 rounded-xl font-bold transition-all shadow-[0_0_20px_rgba(79,70,229,0.3)] flex items-center justify-center gap-2 ${loading ? 'bg-indigo-600/50 cursor-not-allowed' : 'bg-indigo-600 hover:bg-indigo-500 hover:shadow-[0_0_30px_rgba(79,70,229,0.5)]'} text-white`}
        >
          {loading ? (
            <><svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg> Compiling...</>
          ) : "Generate Application"}
        </button>
      </div>

      {/* RIGHT: Live Application Preview */}
      <div className="w-2/3 p-8 overflow-y-auto z-10 custom-scrollbar">
        {config ? (
          <div className="bg-slate-900/60 backdrop-blur-xl border border-white/10 rounded-3xl shadow-2xl min-h-full overflow-hidden animate-[fadeIn_0.5s_ease-out]">
            <nav className="bg-slate-900 border-b border-white/5 p-5 flex justify-between items-center">
              <span className="font-extrabold text-xl text-white tracking-tight">{config.app_name}</span>
              <div className="flex gap-2">
                {config.ui_layout.map((p, idx) => (
                    <span key={p.route} className={`text-sm px-3 py-1.5 rounded-lg ${idx === 0 ? 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/30' : 'text-slate-400 hover:bg-white/5 transition-colors'}`}>
                        {p.title}
                    </span>
                ))}
              </div>
            </nav>
            <div className="p-8">
              {config.ui_layout.map(page => (
                <div key={page.route} className="mb-12">
                  <div className="flex items-center gap-3 mb-6 pb-4 border-b border-white/5">
                      <div className="w-2 h-2 rounded-full bg-indigo-500 shadow-[0_0_10px_rgba(99,102,241,0.8)]"></div>
                      <h3 className="text-2xl font-bold text-white">{page.title}</h3>
                  </div>
                  <div className="grid grid-cols-2 gap-6">
                    {page.components.map((comp, i) => (
                      <div key={i} className="animate-[slideUp_0.5s_ease-out]" style={{ animationFillMode: 'both', animationDelay: `${i * 100}ms` }}>
                        {renderComponent(comp)}
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center h-full text-slate-500">
            <div className="w-24 h-24 mb-6 rounded-full bg-indigo-500/5 flex items-center justify-center border border-indigo-500/10">
                <svg className="w-10 h-10 text-indigo-400/50" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"></path></svg>
            </div>
            <p className="text-lg font-medium text-slate-400">Awaiting Instructions</p>
            <p className="text-sm mt-2 max-w-sm text-center">Enter a prompt on the left to generate an animated dark-theme application preview.</p>
          </div>
        )}
      </div>
      <style>{`
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        @keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        .custom-scrollbar::-webkit-scrollbar { width: 8px; }
        .custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
        .custom-scrollbar::-webkit-scrollbar-thumb { background: #334155; border-radius: 4px; }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #475569; }
      `}</style>
    </div>
  );
};

export default AppCompilerUI;