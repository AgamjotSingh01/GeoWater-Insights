import React, { useState } from "react";
import * as formik from "formik";
import * as yup from "yup";
import { Form, Row } from "react-bootstrap";
import Select2 from "@/Components/Select2";
import a_json from "@/public/a.json"; // Import JSON file

export default function FinalForm() {
    const { Formik } = formik;

    const aquifer = ["Unconfined", "Confined"];
    const rainfall = ["yes", "no"];
    const states = ["Uttar Pradesh_9", "Rajasthan_8", "Maharashtra_27", "Madhya Pradesh_23", "Karnataka_29", "Haryana_6", "Gujarat_24"];

    const [districts, setDistricts] = useState([]);
    const [blocks, setBlocks] = useState([]);

    const schema = yup.object().shape({
        state: yup.string().required("State must be selected"),
        district: yup.string().required("District must be selected"),
        block: yup.string().required("Block must be selected"),
        rainfall_status: yup.string().required("Rainfall status must be selected"),
        aquifer_type: yup.string().required("Aquifer type must be selected"),
    });

    const handleStateChange = (selectedState) => {
        if (a_json[selectedState]) {
            setDistricts(Object.keys(a_json[selectedState]));
            setBlocks([]);
        } else {
            setDistricts([]);
            setBlocks([]);
        }
    };

    const handleDistrictChange = (selectedDistrict, state) => {
        if (a_json[state] && a_json[state][selectedDistrict]) {
            setBlocks(a_json[state][selectedDistrict]);
        } else {
            setBlocks([]);
        }
    };

    return (
        <div className="container">
            <Formik
                validationSchema={schema}
                onSubmit={(values) => {
                    fetch("http://127.0.0.1:5000/predict", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify(values),
                    })
                    .then(async (response) => {
                        if (!response.ok) {
                            throw new Error(`HTTP Error! Status: ${response.status}`);
                        }
                        return response.json();
                    })
                    .then((data) => {
                        localStorage.setItem("predictionData", JSON.stringify(data)); // Store groundwater prediction data
                        window.location.href = "/result"; // Redirect to result page
                    })
                    .catch((error) => console.error("Error in API request:", error));
                }}
                initialValues={{ state: "", district: "", block: "", rainfall_status: "", aquifer_type: "" }}
            >
                {(props) => (
                    <Form noValidate onSubmit={props.handleSubmit}>
                        <Row className="mb-3">
                            <Select2
                                props={props}
                                label="state"
                                id={states}
                                onChange={(value) => {
                                    props.setFieldValue("state", value);
                                    handleStateChange(value);
                                    props.setFieldValue("district", "");
                                    props.setFieldValue("block", "");
                                }}
                            />
                        </Row>
                        <Row className="mb-3">
                            <Select2
                                props={props}
                                label="district"
                                id={districts}
                                onChange={(value) => {
                                    props.setFieldValue("district", value);
                                    handleDistrictChange(value, props.values.state);
                                    props.setFieldValue("block", "");
                                }}
                            />
                        </Row>
                        <Row className="mb-3">
                            <Select2
                                props={props}
                                label="block"
                                id={blocks}
                                onChange={(value) => props.setFieldValue("block", value)}
                            />
                        </Row>
                        <Row className="mb-3">
                            <Select2
                                props={props}
                                label="rainfall_status"
                                id={rainfall}
                                onChange={(value) => props.setFieldValue("rainfall_status", value)}
                            />
                        </Row>
                        <Row className="mb-3">
                            <Select2
                                props={props}
                                label="aquifer_type"
                                id={aquifer}
                                onChange={(value) => props.setFieldValue("aquifer_type", value)}
                            />
                        </Row>
                        <Row className="d-flex justify-content-center">
                            <button className="pushable" type="submit">
                                <span className="shawdow"></span>
                                <span className="edge"></span>
                                <span className="front">Submit</span>
                            </button>
                        </Row>
                    </Form>
                )}
            </Formik>
        </div>
    );
}
