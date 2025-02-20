import PredictionForm from '@/components/PredictionForm';

export default function Home() {
  return (
    <main className="min-h-screen bg-slate-50 py-12">
      <div className="max-w-7xl mx-auto px-4">
        <h1 className="text-4xl font-bold text-center mb-8 text-slate-900">
          Glucolife
        </h1>
        <PredictionForm />
      </div>
    </main>
  );
}
