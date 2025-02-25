import PredictionForm from '@/components/PredictionForm';

export default function Home() {
  return (
    <main className="h-screen overflow-hidden bg-slate-50">
      <div className="h-full max-w-7xl mx-auto px-4 py-6 flex flex-col">
        <h1 className="text-4xl font-bold text-center mb-4 text-slate-900">
          Glucolife
        </h1>
        <div className="flex-1 min-h-0">
          <PredictionForm />
        </div>
      </div>
    </main>
  );
}
