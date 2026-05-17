"use client";

/*
==========================================
WEEK 8 HEALTHCARE FRONTEND
NEXT.JS + TYPESCRIPT + TAILWIND
ALL-IN-ONE SINGLE FILE CODE
==========================================

1. Create Next.js App
npx create-next-app@latest healthcare-dashboard --typescript

2. Install Packages
npm install recharts lucide-react

3. Replace app/page.tsx with this code

4. Run
npm run dev
==========================================
*/

import {
  LayoutDashboard,
  Bell,
  Activity,
  Settings,
  HeartPulse,
  Droplets,
  Thermometer,
  ShieldPlus,
} from "lucide-react";

import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";

const chartData = [
  { day: "Mon", bpm: 72 },
  { day: "Tue", bpm: 78 },
  { day: "Wed", bpm: 75 },
  { day: "Thu", bpm: 85 },
  { day: "Fri", bpm: 80 },
  { day: "Sat", bpm: 76 },
  { day: "Sun", bpm: 79 },
];

export default function Home() {
  return (
    <div className="flex min-h-screen bg-gray-100">

      {/* ================= SIDEBAR ================= */}

      <aside className="w-72 bg-slate-900 text-white p-8">

        <h1 className="text-3xl font-bold mb-12">
          HealthAI
        </h1>

        <nav className="space-y-8">

          <div className="flex items-center gap-4 hover:text-blue-400 cursor-pointer">
            <LayoutDashboard />
            <span className="text-lg">Dashboard</span>
          </div>

          <div className="flex items-center gap-4 hover:text-blue-400 cursor-pointer">
            <Activity />
            <span className="text-lg">Analytics</span>
          </div>

          <div className="flex items-center gap-4 hover:text-blue-400 cursor-pointer">
            <Bell />
            <span className="text-lg">Alerts</span>
          </div>

          <div className="flex items-center gap-4 hover:text-blue-400 cursor-pointer">
            <Settings />
            <span className="text-lg">Settings</span>
          </div>

        </nav>
      </aside>

      {/* ================= MAIN CONTENT ================= */}

      <main className="flex-1">

        {/* ================= HEADER ================= */}

        <header className="bg-white shadow-sm px-10 py-6 flex justify-between items-center">

          <div>
            <h1 className="text-4xl font-bold">
              Patient Monitoring Dashboard
            </h1>

            <p className="text-gray-500 mt-1">
              Real-time healthcare analytics system
            </p>
          </div>

          <div className="flex items-center gap-4">

            <img
              src="https://i.pravatar.cc/50"
              className="rounded-full"
            />

            <div>
              <p className="font-bold">
                Dr. Admin
              </p>

              <p className="text-sm text-gray-500">
                Cardiologist
              </p>
            </div>

          </div>

        </header>

        {/* ================= DASHBOARD BODY ================= */}

        <div className="p-10">

          {/* ================= STAT CARDS ================= */}

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">

            {/* HEART RATE */}

            <div className="bg-white rounded-2xl p-6 shadow-lg">

              <div className="flex justify-between items-center">

                <div>
                  <p className="text-gray-500">
                    Heart Rate
                  </p>

                  <h2 className="text-4xl font-bold mt-2">
                    78 BPM
                  </h2>
                </div>

                <div className="bg-red-100 p-4 rounded-full">
                  <HeartPulse className="text-red-500" />
                </div>

              </div>

            </div>

            {/* BLOOD PRESSURE */}

            <div className="bg-white rounded-2xl p-6 shadow-lg">

              <div className="flex justify-between items-center">

                <div>
                  <p className="text-gray-500">
                    Blood Pressure
                  </p>

                  <h2 className="text-4xl font-bold mt-2">
                    120/80
                  </h2>
                </div>

                <div className="bg-blue-100 p-4 rounded-full">
                  <Droplets className="text-blue-500" />
                </div>

              </div>

            </div>

            {/* TEMPERATURE */}

            <div className="bg-white rounded-2xl p-6 shadow-lg">

              <div className="flex justify-between items-center">

                <div>
                  <p className="text-gray-500">
                    Temperature
                  </p>

                  <h2 className="text-4xl font-bold mt-2">
                    98.6°F
                  </h2>
                </div>

                <div className="bg-orange-100 p-4 rounded-full">
                  <Thermometer className="text-orange-500" />
                </div>

              </div>

            </div>

            {/* OXYGEN */}

            <div className="bg-white rounded-2xl p-6 shadow-lg">

              <div className="flex justify-between items-center">

                <div>
                  <p className="text-gray-500">
                    Oxygen Level
                  </p>

                  <h2 className="text-4xl font-bold mt-2">
                    98%
                  </h2>
                </div>

                <div className="bg-green-100 p-4 rounded-full">
                  <ShieldPlus className="text-green-500" />
                </div>

              </div>

            </div>

          </div>

          {/* ================= CHART + SIDE PANELS ================= */}

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">

            {/* ================= CHART ================= */}

            <div className="lg:col-span-2 bg-white rounded-2xl shadow-lg p-8">

              <h2 className="text-3xl font-bold mb-6">
                Weekly Heart Rate Analysis
              </h2>

              <ResponsiveContainer width="100%" height={400}>

                <LineChart data={chartData}>

                  <CartesianGrid strokeDasharray="3 3" />

                  <XAxis dataKey="day" />

                  <YAxis />

                  <Tooltip />

                  <Line
                    type="monotone"
                    dataKey="bpm"
                    stroke="#2563EB"
                    strokeWidth={5}
                  />

                </LineChart>

              </ResponsiveContainer>

            </div>

            {/* ================= RIGHT PANELS ================= */}

            <div className="space-y-8">

              {/* AI PREDICTION */}

              <div className="bg-white rounded-2xl shadow-lg p-6">

                <h2 className="text-2xl font-bold mb-6">
                  AI Predictive Insights
                </h2>

                <div className="bg-red-100 border border-red-300 rounded-xl p-5">

                  <h3 className="text-red-600 font-bold text-xl">
                    High Risk Detected
                  </h3>

                  <p className="mt-3 text-gray-700">
                    Patient may experience elevated blood pressure within 24 hours.
                  </p>

                </div>

                <div className="mt-5 bg-green-100 border border-green-300 rounded-xl p-5">

                  <h3 className="text-green-600 font-bold text-xl">
                    Oxygen Stable
                  </h3>

                  <p className="mt-3 text-gray-700">
                    Oxygen saturation levels are within normal range.
                  </p>

                </div>

              </div>

              {/* NOTIFICATIONS */}

              <div className="bg-white rounded-2xl shadow-lg p-6">

                <h2 className="text-2xl font-bold mb-6">
                  Notifications
                </h2>

                <div className="space-y-4">

                  <div className="bg-blue-100 rounded-xl p-4">
                    Medication reminder scheduled for 6 PM.
                  </div>

                  <div className="bg-yellow-100 rounded-xl p-4">
                    Heart rate slightly elevated during exercise.
                  </div>

                  <div className="bg-red-100 rounded-xl p-4">
                    Blood pressure exceeded safe threshold.
                  </div>

                  <div className="bg-green-100 rounded-xl p-4">
                    Daily health report generated successfully.
                  </div>

                </div>

              </div>

            </div>

          </div>

        </div>

      </main>

    </div>
  );
}