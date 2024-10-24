"use client";
import React, { useEffect, useState } from "react";
import { DocumentData } from "./interface";
import { useMutation, useQuery } from "@tanstack/react-query";
import Image from "next/image";
import Link from "next/link";
import { IoIosArrowDropright } from "react-icons/io";

export type SelectedDocument = {
  id?: string;
  document?: string;
  semantic: number;
};

export default function TextPage() {
  const { data: categories, isSuccess: categoriesSuccess } = useQuery({
    queryKey: ["getCategory"],
    queryFn: async () => {
      const endpoint = `${process.env["NEXT_PUBLIC_API_URL"]}/text/category`;
      console.log(endpoint);
      const response = await fetch(endpoint, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
        cache: "no-cache",
      });
      const data: DocumentData = await response.json();
      return data;
    },
  });

  const [currentCategory, setCurrentCategory] = useState<string>(
    categoriesSuccess ? categories.documents[0] : ""
  );

  // Update the current category only when categories are successfully fetched
  useEffect(() => {
    if (categoriesSuccess && categories?.documents?.length > 0) {
      setCurrentCategory(categories.documents[0]); // Set the first category as default
    }
  }, [categoriesSuccess, categories]);

  const [selectedDocuments, setSelectedDocuments] = useState<
    SelectedDocument[]
  >([]);

  console.log("Selected Documents: ", selectedDocuments);
  console.log("Current: ", currentCategory);

  const { data: documentsData, isLoading: documentsLoading } = useQuery({
    queryKey: ["documents", currentCategory],
    queryFn: async () => {
      const response = await fetch(
        `${
          process.env["NEXT_PUBLIC_API_URL"] as string
        }/text?category=${currentCategory}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
          cache: "no-cache",
        }
      );
      const data: DocumentData = await response.json();
      return data;
    },
    enabled: !!categories,
  });

  const mutate = useMutation({
    mutationKey: ["resultValues"],
    mutationFn: async () => {
      const response = await fetch(
        `${process.env["NEXT_PUBLIC_API_URL"] as string}/text/similar`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          cache: "no-cache",
          body: JSON.stringify({
            data: selectedDocuments,
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

  const handleCategoryChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    mutate.reset();
    setCurrentCategory(e.target.value);
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
            id: document_id,
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
        <h1 className="text-3xl font-poppins my-4">Sentence Similarity</h1>
        <Link
          className="btn btn-ghost rounded-full h-10 w-[56px] ml-2"
          href={"/text-image"}
        >
          <IoIosArrowDropright
            size={32}
            className="text-white w-full h-full"
          ></IoIosArrowDropright>
        </Link>
      </div>
      <div className="h-full w-full flex lg:flex-row flex-col">
        <div className="lg:h-full lg:w-1/3 lg:border-r-[1px] border-slate-400 w-full flex flex-col justify-start items-start pr-4">
          <div className="w-full flex flex-row justify-between items-center">
            <div className="w-1/2 h-full flex flex-col justify-start items-center">
              {categoriesSuccess ? (
                <>
                  <div className="label">
                    <span className="label-text">Select a category</span>
                  </div>
                  <select
                    name="category"
                    id="category"
                    value={currentCategory}
                    onChange={handleCategoryChange}
                    className="w-full select select-bordered max-w-xs mb-4 bg-slate-950"
                  >
                    {categories.documents.map((category, index) => (
                      <option key={index} value={category}>
                        {category}
                      </option>
                    ))}
                  </select>
                </>
              ) : (
                <div className="w-full h-full flex justify-center items-center">
                  <span className="loading loading-spinner bg-primary"></span>
                </div>
              )}
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
                const doc_id = documentsData.ids[index];
                return (
                  <div
                    key={doc_id}
                    className={`rounded-md flex flex-col justify-center items-center bg-slate-900 h-56 hover:scale-105 cursor-pointer duration-500
                                ${
                                  selectedDocuments.some((document) => {
                                    return (
                                      document.document ===
                                      documentsData.documents[index]
                                    );
                                  })
                                    ? "border-[1px] border-primary"
                                    : ""
                                }`}
                    onClick={() => toggleActiveDocument(index, doc_id)}
                  >
                    <div className="w-full flex flex-col justify-center items-center h-3/4">
                      <h1 className="text-center font-light text-base text-white ">
                        {doc}
                      </h1>
                    </div>
                    <label>
                      <span className="label-text text-slate-400 font-light mt-2 ">
                        Semantic (%)
                      </span>
                    </label>
                    <select
                      id={`semantic-${index}`}
                      className="select select-bordered w-28 2xl:w-48 h-1/4 my-1  max-w-xs"
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
            {mutate.data.documents.map((doc, index) => (
              <div
                key={index}
                className="rounded-md flex flex-col justify-center items-center bg-slate-900 h-28 w-56 sm:w-1/2 lg:w-1/3 cursor-pointer"
              >
                <div className="w-full h-full flex flex-col justify-center items-center">
                  <h1 className="text-center font-light text-base text-white ">
                    {doc}
                  </h1>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="lg:h-full lg:w-2/3 w-full h-full flex flex-col justify-center items-center overflow-y-auto">
            <div className="w-[300px] h-[300px] relative">
              <Image
                src={"illustration/text.svg"}
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
