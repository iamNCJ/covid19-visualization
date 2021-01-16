import ReactEcharts from "echarts-for-react";
import { useEffect, useState } from "react";
import mini from "./ProvinceCaseMini.json";
import large from "./ProvinceCaseLarge.json";

export default function ProvinceCase(props) {
  let [option, SetOption] = useState(undefined);

  const initOption = () => ({
    visualMap: {
      type: "continuous",
      min: 0,
      max: 10,
      inRange: {
        color: ["#2D5F73", "#538EA6", "#F2D1B3", "#F2B8A2", "#F28C8C"],
      },
    },
    series: {
      type: "sunburst",
      data: mini,
      radius: [0, "90%"],
      label: [
        {
          rotate: "radial",
        },
      ]
    },
  });

  useEffect(() => {
    SetOption(initOption());
  }, []);

  return (
    <div className="province-case-comp">
      {option && (
        <ReactEcharts option={option} style={{ height: props.height ?? 800 }} />
      )}
    </div>
  );
}
