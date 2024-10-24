"use client";

import { useState } from "react";
import Link from "next/link";
import { IoIosArrowDropleft } from "react-icons/io";
import { useMutation, useQuery } from "@tanstack/react-query";
import { DocumentData } from "../text/interface";
import Image from "next/image";

export interface SelectedDocument {
  id?: string;
  document?: string;
  semantic: number;
}

export default function TextImagePage() {
  const modalities = ["text", "image"];
  const [currentModality, setCurrentModality] = useState<string>(modalities[0]);
  const [selectedDocuments, setSelectedDocuments] = useState<
    SelectedDocument[]
  >([]);

  console.log("Selected: ", selectedDocuments);
  console.log("Modality: ", currentModality);
  const { data: documentsData, isLoading: documentsLoading } = useQuery({
    queryKey: ["texts"],
    queryFn: async () => {
      const response = await fetch(
        `${process.env["NEXT_PUBLIC_API_URL"] as string}/images/text`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
          cache: "no-cache",
        }
      );
      const data: DocumentData = await response.json();
      console.log(data);
      return data;
    },
  });

  const mutate = useMutation({
    mutationKey: ["resultTextImages"],
    mutationFn: async () => {
      const response = await fetch(
        `${process.env["NEXT_PUBLIC_API_URL"] as string}/images/results`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          cache: "no-cache",
          body: JSON.stringify({
            data: {
              modality: currentModality,
              documents: selectedDocuments,
            },
          }),
        }
      );
      const data: DocumentData = await response.json();
      return data;
    },
  });

  const handleReset = () => {
    mutate.reset();
    // Reset the value of all semantic select dropdowns to 100
    selectedDocuments.forEach((doc) => {
      const semanticElement = document.querySelector(
        `#semantic-${doc.id}`
      ) as HTMLSelectElement;
      if (semanticElement) {
        semanticElement.value = "100"; // Reset to 100
      }
    });
    setSelectedDocuments([]);
  };

  const handleModalityChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    mutate.reset();
    setCurrentModality(e.target.value);
  };

  const toggleActiveDocument = (index: number, document_id: string) => {
    setSelectedDocuments((prevActiveDocuments) => {
      if (prevActiveDocuments.some((doc) => doc.id === document_id)) {
        return prevActiveDocuments.filter((doc) => doc.id !== document_id);
      } else {
        const semanticValue =
          Number(
            (
              document.querySelector(
                `#semantic-${document_id}`
              ) as HTMLSelectElement
            ).value
          ) / 100;
        return [
          ...prevActiveDocuments,
          {
            id: documentsData?.ids[index],
            document: documentsData?.documents[index],
            semantic: semanticValue,
          },
        ];
      }
    });
  };

  const handleSemanticChange = (
    e: React.ChangeEvent<HTMLSelectElement>,
    doc: string
  ) => {
    const semanticValue = Number(e.target.value) / 100;

    const newValue: SelectedDocument[] = selectedDocuments.map((item) => {
      if (item.document === doc) {
        return {
          ...item,
          semantic: semanticValue,
        };
      }
      return item;
    });

    setSelectedDocuments(newValue);
  };

  return (
    <div className="container w-full h-full m-auto flex flex-col overflow-hidden">
      <div className="h-1/6 w-full flex justify-center items-center">
        <Link
          className="btn btn-ghost rounded-full h-10 w-[56px] ml-2"
          href={"/text"}
        >
          <IoIosArrowDropleft
            size={32}
            className="text-white w-full h-full"
          ></IoIosArrowDropleft>
        </Link>
        <h1 className="text-3xl font-poppins my-4">Image-Text Similarity</h1>
      </div>
      <div className="h-full w-full flex lg:flex-row flex-col">
        <div className="lg:h-full lg:w-1/3 lg:border-r-[1px] border-slate-400 w-full flex flex-col justify-start items-start pr-4">
          <div className="w-full flex flex-row justify-between items-center">
            <div className="w-1/2 h-full flex flex-col justify-star items-center">
              <div className="label">
                <span className="label-text">Select a modality</span>
              </div>
              <select
                name="modality"
                id="modality"
                value={currentModality}
                onChange={handleModalityChange}
                className="w-full select select-bordered max-w-xs mb-4 bg-slate-950"
              >
                {modalities.map((modality, index) => (
                  <option key={index} value={modality}>
                    {modality}
                  </option>
                ))}
              </select>
            </div>

            <div className="w-1/2 h-full flex items-center justify-end">
              <button
                className="btn btn-primary w-36 rounded-md mt-6 text-lg font-semibold"
                onClick={() => mutate.mutate()}
              >
                Search
              </button>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4 overflow-y-auto lg:h-4/6 h-[300px] p-2">
            {documentsLoading ? (
              <div className="flex flex-col justify-center items-center">
                <h1>Loading...</h1>
              </div>
            ) : documentsData ? (
              documentsData.documents.map((doc, index) => {
                const doc_id = Number(documentsData.ids[index]);
                return (
                  <div
                    key={doc_id}
                    className={`rounded-md flex flex-col justify-center items-center bg-slate-900 h-96 hover:scale-105 cursor-pointer duration-500
                                ${
                                  selectedDocuments.some((document) => {
                                    return document.document === doc;
                                  })
                                    ? "border-[1px] border-primary"
                                    : ""
                                }`}
                    onClick={() =>
                      toggleActiveDocument(index, doc_id.toString())
                    }
                  >
                    <div className="w-full flex flex-col justify-center items-center h-full rounded-md">
                      <div className="relative w-full h-48">
                        <Image
                          src={`/preprocessed/${doc_id}.jpg`}
                          fill={true}
                          alt={doc}
                          className="object-fit rounded-t-md"
                        />
                      </div>
                      <div className="h-32 w-full flex justify-center items-center">
                        <h1 className="text-center font-light text-sm text-white ">
                          {doc}
                        </h1>
                      </div>

                      <label>
                        <span className="label-text text-slate-400 font-light mt-2 h-4 ">
                          Semantic (%)
                        </span>
                      </label>
                      <select
                        id={`semantic-${doc_id}`}
                        className="select select-bordered w-28 2xl:w-48 h-12 my-1  max-w-xs"
                        defaultValue={100}
                        onChange={(e) => handleSemanticChange(e, doc)}
                      >
                        {Array.from({ length: 11 }, (_, i) => i * 10).map(
                          (value) => (
                            <option key={value} value={value}>
                              {value}
                            </option>
                          )
                        )}
                      </select>
                    </div>
                  </div>
                );
              })
            ) : null}
          </div>
          <div className="w-full flex items-center justify-center">
            <button
              className="btn btn-secondary btn-outline lg:w-full w-56 rounded-md mt-6 text-lg font-semibold"
              onClick={handleReset}
            >
              Reset
            </button>
          </div>
        </div>

        {mutate.isPending ? (
          <div className="flex flex-col justify-center items-center">
            <h1>Loading...</h1>
          </div>
        ) : mutate.isSuccess && mutate.data ? (
          <div className="lg:w-2/3 w-full flex flex-row flex-wrap lg:justify-start justify-center items-start mt-4 lg:py-16 lg:px-4 gap-4 overflow-y-auto">
            {mutate.data.documents.map((doc, index) => {
              const found_id = Number(mutate.data.ids[index]);
              return (
                <div
                  key={found_id}
                  className="rounded-md flex flex-col justify-center items-center bg-slate-900 w-64 sm:w-1/2 lg:w-1/3 cursor-pointer"
                >
                  <div className="w-full h-full flex flex-col justify-center items-center">
                    <div className="relative w-full h-48">
                      <Image
                        src={`/preprocessed/${found_id}.jpg`}
                        fill={true}
                        className="object-fit"
                        alt={doc}
                      />
                    </div>
                    <h1 className="text-center font-light text-base text-white ">
                      {doc}
                    </h1>
                  </div>
                </div>
              );
            })}
          </div>
        ) : (
          <div className="lg:h-full lg:w-2/3 w-full h-full flex flex-col justify-center items-center overflow-y-auto">
            <div className="w-[300px] h-[300px] relative">
              <Image
                src={"illustration/image.svg"}
                alt="Text"
                fill={true}
                className="object-fit"
              ></Image>
            </div>

            <h2 className="w-full lg:w-96 h-12 text-center text-lg text-white font-poppins my-4">
              Your sentences will be displayed here
            </h2>
          </div>
        )}
      </div>
    </div>
  );
}
