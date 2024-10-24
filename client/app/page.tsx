import Link from "next/link";

export default function Home() {
  return (
    <div className="w-screen h-screen flex flex-col justify-center items-center">
      <div className="container flex flex-col justify-center items-center">
        <h1 className="text-4xl font-semibold tracking-widest font-poppins">
          CreatiVec
        </h1>
        <p className="mt-4 mb-8 w-[360px] md:w-[400px] text-sm text-center font-light tracking-wider font-poppins text-slate-300 ">
          An application to demonstrate content discovery throught semantic
          blend with embedding vectors.
        </p>
        <div
          className="rounded-lg m-2 max-w-screen md:w-96 h-56
      flex flex-col justify-center items-center bg-gradient-to-tr from-slate-800 via-slate-900 to-slate-950 shadow-slate-400/40 shadow-md"
        >
          <h1 className="justify-center text-2xl font-semibold mb-4">
            Choose a modality
          </h1>
          <div className="w-full flex flex-row flex-wrap justify-evenly items-center">
            <Link
              href={"/text"}
              className="btn btn-primary font-poppins w-36 tracking-wider hover:scale-105 duration-500"
            >
              Text
            </Link>
            <Link
              href={"/text-image"}
              className="btn btn-primary font-poppins w-36 tracking-wider hover:scale-105 duration-500"
            >
              Multimodal
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
