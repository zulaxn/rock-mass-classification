
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Rock Mass Classification",
    page_icon="⛰️",
    layout="wide"
)

st.title("⛰️ ROCK MASS CLASSIFICATION")
st.caption("RMR | GSI | Q-System")
st.divider()

menu = st.sidebar.radio(
    "Үндсэн цэс",
    [
        "Нүүр хуудас",
        "RMR үнэлгээ",
        "GSI үнэлгээ",
        "Q-System үнэлгээ",
        "Харьцуулалт",
    ]
)

if menu == "Нүүр хуудас":
    st.header("Чулуулгийн массивын ангиллын систем")
    st.write(
        "Энэхүү программ нь чулуулгийн массивын "
        "геомеханикийн үнэлгээг RMR, GSI болон Q-System "
        "аргаар гүйцэтгэнэ."
    )
    st.info("Зүүн талын цэснээс үнэлгээний төрлөө сонгоно уу.")

elif menu == "RMR үнэлгээ":

    st.header("RMR үнэлгээ")
    st.write("Bieniawski (1989) classification system")

    st.subheader("1. Чулуулгийн бат бэх (UCS)")

    ucs = st.number_input(
        "Нэг тэнхлэгийн шахалтын бат бэх (MPa)",
        min_value=0.0,
        max_value=1000.0,
        value=100.0,
        step=1.0
    )

    if ucs > 250:
        ucs_score = 15
    elif ucs >= 100:
        ucs_score = 12
    elif ucs >= 50:
        ucs_score = 7
    elif ucs >= 25:
        ucs_score = 4
    elif ucs >= 5:
        ucs_score = 2
    elif ucs >= 1:
        ucs_score = 1
    else:
        ucs_score = 0

    st.caption(f"UCS оноо: {ucs_score}/15")

    st.subheader("2. Чулуулгийн чанарын үзүүлэлт (RQD)")

    rqd = st.number_input(
        "RQD (%)",
        min_value=0.0,
        max_value=100.0,
        value=75.0,
        step=1.0
    )

    if rqd >= 90:
        rqd_score = 20
    elif rqd >= 75:
        rqd_score = 17
    elif rqd >= 50:
        rqd_score = 13
    elif rqd >= 25:
        rqd_score = 8
    else:
        rqd_score = 3

    st.caption(f"RQD оноо: {rqd_score}/20")

    st.subheader("3. Тасалдалуудын хоорондын зай")

    spacing = st.number_input(
        "Дундаж зай (метр)",
        min_value=0.001,
        max_value=10.0,
        value=0.6,
        step=0.1
    )

    if spacing > 2:
        spacing_score = 20
    elif spacing >= 0.6:
        spacing_score = 15
    elif spacing >= 0.2:
        spacing_score = 10
    elif spacing >= 0.06:
        spacing_score = 8
    else:
        spacing_score = 5

    st.caption(f"Зайн оноо: {spacing_score}/20")

    st.subheader("4. Тасалдалуудын гадаргын нөхцөл")

    condition_options = {
        "Маш барзгар, үргэлжилсэн бус, зай завсаргүй, өгөршөөгүй": 30,
        "Бага зэрэг барзгар, зай завсар <1 мм, бага зэрэг өгөршсөн": 25,
        "Бага зэрэг барзгар, зай завсар <1 мм, хүчтэй өгөршсөн": 20,
        "Гөлгөржсөн эсвэл дүүргэгч <5 мм, зай завсар 1–5 мм, үргэлжилсэн": 10,
        "Зөөлөн дүүргэгч >5 мм эсвэл зай завсар >5 мм, үргэлжилсэн": 0
    }

    condition = st.selectbox(
        "Тасалдлын нөхцөлийг сонгоно уу",
        list(condition_options.keys())
    )

    condition_score = condition_options[condition]
    st.caption(f"Нөхцөлийн оноо: {condition_score}/30")

    st.subheader("5. Газрын доорх усны нөхцөл")

    water_options = {
        "Бүрэн хуурай": 15,
        "Чийглэг": 10,
        "Нойтон": 7,
        "Ус дусалж байгаа": 4,
        "Ус урсаж байгаа": 0
    }

    water = st.selectbox(
        "Усны нөхцөл",
        list(water_options.keys())
    )

    water_score = water_options[water]
    st.caption(f"Усны оноо: {water_score}/15")

    st.divider()
    st.subheader("6. Тасалдалуудын чиглэлийн нөлөөлөл")

    structure = st.selectbox(
        "Үнэлэх байгууламжийн төрөл",
        [
            "Налуу (Slope)",
            "Туннель ба уурхай (Tunnels and mines)",
            "Суурь (Foundations)"
        ]
    )

    orientation_options = [
        "Маш таатай (Very favourable)",
        "Таатай (Favourable)",
        "Дунд зэрэг (Fair)",
        "Тааламжгүй (Unfavourable)",
        "Маш тааламжгүй (Very unfavourable)"
    ]

    orientation_ratings = {
        "Налуу (Slope)": [0, -5, -25, -50, -60],
        "Туннель ба уурхай (Tunnels and mines)": [0, -2, -5, -10, -12],
        "Суурь (Foundations)": [0, -2, -7, -15, -25]
    }

    orientation = st.selectbox(
        "Тасалдалуудын чиглэлийн үнэлгээ",
        orientation_options
    )

    orientation_index = orientation_options.index(orientation)
    orientation_score = orientation_ratings[structure][orientation_index]

    st.caption(f"Чиглэлийн засварын оноо: {orientation_score}")

    st.divider()

    basic_rmr = (
        ucs_score
        + rqd_score
        + spacing_score
        + condition_score
        + water_score
    )

    final_rmr = basic_rmr + orientation_score

    if final_rmr > 80:
        rock_class = "I - Маш сайн"
    elif final_rmr > 60:
        rock_class = "II - Сайн"
    elif final_rmr > 40:
        rock_class = "III - Дунд зэрэг"
    elif final_rmr > 20:
        rock_class = "IV - Муу"
    else:
        rock_class = "V - Маш муу"
    st.session_state["basic_rmr"] = basic_rmr
    st.session_state["final_rmr"] = final_rmr
    st.session_state["rock_class"] = rock_class

    st.header("RMR ҮНЭЛГЭЭНИЙ ҮР ДҮН")

    col1, col2, col3 = st.columns(3)

    col1.metric("Basic RMR", f"{basic_rmr}/100")
    col2.metric("Orientation adjustment", orientation_score)
    col3.metric("Final RMR", final_rmr)

    st.success(f"Чулуулгийн массивын ангилал: {rock_class}")

    result_table = pd.DataFrame({
        "Үзүүлэлт": [
            "UCS",
            "RQD",
            "Тасалдалуудын хоорондын зай",
            "Тасалдалуудын гадаргын нөхцөл",
            "Газрын доорх ус",
            "Чиглэлийн засвар"
        ],
        "Оноо": [
            ucs_score,
            rqd_score,
            spacing_score,
            condition_score,
            water_score,
            orientation_score
        ]
    })

    st.subheader("Онооны дэлгэрэнгүй")
    st.dataframe(result_table, use_container_width=True)

    st.caption(
        "Эх сурвалж: Bieniawski (1989), "
        "Engineering Rock Mass Classifications. "
        "Урьдчилсан үнэлгээний зориулалттай."
    )


elif menu == "GSI үнэлгээ":

    st.header("GSI үнэлгээ")
    st.caption("Geological Strength Index | Hoek & Marinos (2000)")

    st.subheader("1. Чулуулгийн массивын бүтэц")

    structure_options = {
        "Intact or Massive": "Цөөн, хоорондоо хол зайтай тасалдалтай, эсвэл массивлаг чулуулаг",
        "Blocky": "Гурван огтлолцсон ан цавын системээр үүссэн, сайн түгжигдсэн блоклог массив",
        "Very Blocky": "Дөрөв ба түүнээс олон ан цавын системтэй, олон талт өнцөглөг блокууд",
        "Blocky / Disturbed / Seamy": "Олон тасалдлаар хуваагдсан, эвхэгдсэн, хөндөгдсөн блоклог массив",
        "Disintegrated": "Хүчтэй бутарч, блок хоорондын түгжээ муудсан массив",
        "Laminated / Sheared": "Ойр зайтай сул үелэл, шистлэг болон шилжрэлтийн хавтгайтай массив"
    }

    structure = st.selectbox(
        "Бүтцийн ангилал сонгох",
        list(structure_options.keys())
    )

    st.info(structure_options[structure])

    st.divider()

    st.subheader("2. Тасалдалуудын гадаргын нөхцөл")

    surface_options = {
        "Very Good": "Маш барзгар, шинэхэн, өгөршөөгүй гадаргуу",
        "Good": "Барзгар, бага зэрэг өгөршсөн, төмрийн толботой гадаргуу",
        "Fair": "Гөлгөр, дунд зэрэг өгөршсөн болон өөрчлөгдсөн гадаргуу",
        "Poor": "Гулгамтгай, хүчтэй өгөршсөн, нягтарсан бүрхүүл эсвэл дүүргэгчтэй гадаргуу",
        "Very Poor": "Гулгамтгай, хүчтэй өгөршсөн, зөөлөн шаварлаг бүрхүүл эсвэл дүүргэгчтэй гадаргуу"
    }

    surface = st.selectbox(
        "Гадаргын нөхцөл сонгох",
        list(surface_options.keys())
    )

    st.info(surface_options[surface])

    st.divider()

    st.subheader("3. GSI-ийн үнэлгээний муж")

    st.write(
        "Дээр сонгосон бүтцийн болон гадаргын нөхцөлийг "
        "Hoek–Marinos (2000)-ийн GSI графиктай тулгаж, "
        "тохирох үнэлгээний мужийг сонгоно уу."
    )

    gsi_range = st.slider(
        "GSI-ийн доод ба дээд утга",
        min_value=10,
        max_value=90,
        value=(35, 45),
        step=1
    )

    gsi_min = gsi_range[0]
    gsi_max = gsi_range[1]
    gsi_average = (gsi_min + gsi_max) / 2
    st.session_state["gsi_min"] = gsi_min
    st.session_state["gsi_max"] = gsi_max
    st.session_state["gsi_average"] = gsi_average
    st.session_state["gsi_structure"] = structure
    st.session_state["gsi_surface"] = surface

    st.divider()

    st.header("GSI ҮНЭЛГЭЭНИЙ ҮР ДҮН")

    col1, col2, col3 = st.columns(3)

    col1.metric("Доод утга", gsi_min)
    col2.metric("Дундаж GSI", f"{gsi_average:.1f}")
    col3.metric("Дээд утга", gsi_max)

    st.success(
        f"Чулуулгийн массивын GSI үнэлгээ: "
        f"{gsi_min} – {gsi_max}"
    )

    st.subheader("Үнэлгээний дэлгэрэнгүй")

    gsi_table = pd.DataFrame({
        "Үзүүлэлт": [
            "Чулуулгийн массивын бүтэц",
            "Тасалдалуудын гадаргын нөхцөл",
            "GSI доод утга",
            "GSI дээд утга",
            "Дундаж GSI"
        ],
        "Үнэлгээ": [
            structure,
            surface,
            gsi_min,
            gsi_max,
            gsi_average
        ]
    })

    st.dataframe(gsi_table, use_container_width=True)

    st.warning(
        "Анхааруулга: GSI нь графикаар болон геологийн "
        "ажиглалтаар үнэлэгддэг. Энэ программд бүтцийн "
        "болон гадаргын ангиллыг сонгоод, графикаас "
        "тогтоосон GSI мужийг хэрэглэгч оруулна. "
        "Автомат ангиллын утга гэж үзэж болохгүй."
    )

    st.caption(
        "Эх сурвалж: Hoek and Marinos (2000), "
        "Geological Strength Index for Jointed Rocks."
    )


elif menu == "Q-System үнэлгээ":

    st.header("Q-System үнэлгээ")
    st.caption("Barton, Lien & Lunde (1974)")

    st.subheader("1. Чулуулгийн чанарын үзүүлэлт (RQD)")

    rqd_q = st.number_input(
        "RQD (%)",
        min_value=0.0,
        max_value=100.0,
        value=75.0,
        step=1.0,
        key="q_rqd"
    )

    rqd_used = max(rqd_q, 10.0)

    if rqd_q <= 10:
        st.warning("Q тооцоонд RQD ≤ 10 үед RQD = 10 гэж авна.")

    st.subheader("2. Ан цавын системийн тоо (Jn)")

    jn_options = {
        "Массивлаг, цөөн тасалдалтай": 0.5,
        "Нэг ан цавын систем": 2,
        "Нэг систем + санамсаргүй ан цав": 3,
        "Хоёр ан цавын систем": 4,
        "Хоёр систем + санамсаргүй ан цав": 6,
        "Гурван ан цавын систем": 9,
        "Гурван систем + санамсаргүй ан цав": 12,
        "Дөрөв ба түүнээс олон систем": 15,
        "Бутарсан, үйрмэг чулуулаг": 20
    }

    jn_name = st.selectbox(
        "Ан цавын системийн тоог сонгох",
        list(jn_options.keys())
    )
    jn = jn_options[jn_name]

    st.subheader("3. Ан цавын гадаргуугийн барзгаршил (Jr)")

    jr_options = {
        "Тасалдсан ан цав": 4.0,
        "Барзгар, долгиолог": 3.0,
        "Гөлгөр, долгиолог": 2.0,
        "Гулгамтгай, долгиолог": 1.5,
        "Барзгар, хавтгай": 1.5,
        "Гөлгөр, хавтгай": 1.0,
        "Гулгамтгай, хавтгай": 0.5
    }

    jr_name = st.selectbox(
        "Ан цавын гадаргууг сонгох",
        list(jr_options.keys())
    )
    jr = jr_options[jr_name]

    st.subheader("4. Ан цавын өөрчлөлт, өгөршил (Ja)")

    ja_options = {
        "Нягт барьцалдсан, өөрчлөлтгүй": 0.75,
        "Өөрчлөлтгүй, ан цавын ханатай шууд хүрэлцсэн": 1.0,
        "Бага зэрэг өөрчлөгдсөн эрдсийн бүрхүүлтэй": 2.0,
        "Элсэрхэг, шаварлаг нимгэн бүрхүүлтэй": 3.0,
        "Зөөлөн шаварлаг эрдсийн бүрхүүлтэй": 4.0,
        "Нимгэн шаварлаг дүүргэгчтэй": 4.0,
        "Дунд зэргийн шаварлаг дүүргэгчтэй": 6.0,
        "Зузаан шаварлаг дүүргэгчтэй": 8.0
    }

    ja_name = st.selectbox(
        "Ан цавын өөрчлөлтийн нөхцөлийг сонгох",
        list(ja_options.keys())
    )
    ja = ja_options[ja_name]

    st.subheader("5. Ан цавын усны нөлөөлөл (Jw)")

    jw_options = {
        "Хуурай эсвэл бага хэмжээний усны нөлөө": 1.0,
        "Дунд зэргийн усны нөлөө": 0.66,
        "Их хэмжээний усны нөлөө": 0.5,
        "Маш их хэмжээний усны нөлөө": 0.2,
        "Онцгой өндөр даралттай усны нөлөө": 0.1
    }

    jw_name = st.selectbox(
        "Усны нөхцөлийг сонгох",
        list(jw_options.keys())
    )
    jw = jw_options[jw_name]

    st.subheader("6. Хүчдэлийн бууралтын коэффициент (SRF)")

    srf = st.number_input(
        "SRF утга",
        min_value=0.1,
        max_value=100.0,
        value=1.0,
        step=0.1
    )

    st.caption(
        "SRF-ийг геологийн сул бүс, чулуулгийн хүчдэл, "
        "гулсалт, бутрал болон малталтын нөхцөлд үндэслэн "
        "Q-system-ийн хүснэгтээс сонгоно."
    )

    st.divider()

        
    if jn > 0 and ja > 0 and srf > 0:

        q_value = (
            (rqd_used / jn)
            * (jr / ja)
            * (jw / srf)
        )

        a = rqd_used / jn
        b = jr / ja
        c = jw / srf

        if q_value >= 400:
            q_class = "Онцгой сайн"
        elif q_value >= 100:
            q_class = "Маш сайн"
        elif q_value >= 40:
            q_class = "Сайн"
        elif q_value >= 10:
            q_class = "Дунд зэрэг"
        elif q_value >= 4:
            q_class = "Муу"
        elif q_value >= 1:
            q_class = "Маш муу"
        elif q_value >= 0.1:
            q_class = "Онцгой муу"
        elif q_value >= 0.01:
            q_class = "Маш онцгой муу"
        else:
            q_class = "Хэт онцгой муу"
        st.session_state["q_value"] = q_value
        st.session_state["q_class"] = q_class

        st.header("Q-SYSTEM ҮНЭЛГЭЭНИЙ ҮР ДҮН")

        col1, col2 = st.columns(2)
        col1.metric("Q утга", f"{q_value:.3f}")
        col2.metric("Чулуулгийн массивын чанар", q_class)

        st.subheader("Тооцооллын үзүүлэлтүүд")

        q_table = pd.DataFrame({
            "Үзүүлэлт": ["RQD", "Jn", "Jr", "Ja", "Jw", "SRF"],
            "Утга": [rqd_used, jn, jr, ja, jw, srf]
        })

        st.dataframe(q_table, use_container_width=True)

        st.subheader("Q-System-ийн гурван үндсэн харьцаа")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Degree of Jointing", f"{a:.3f}")
            st.markdown("**RQD / Jn**")
            st.write(
                "Чулуулгийн массивын ан цавшилтын зэрэг, "
                "блокийн хэмжээ болон бүтцийн хуваагдлыг илэрхийлнэ."
            )

        with col2:
            st.metric("Joint Friction", f"{b:.3f}")
            st.markdown("**Jr / Ja**")
            st.write(
                "Ан цавын гадаргуугийн барзгаршил, "
                "өгөршил болон үрэлтийн эсэргүүцлийг илэрхийлнэ."
            )

        with col3:
            st.metric("Joint Water Reduction / Stress", f"{c:.3f}")
            st.markdown("**Jw / SRF**")
            st.write(
                "Ан цавын усны нөлөөлөл болон "
                "чулуулгийн хүчдэлийн нөхцөлийн нөлөөг илэрхийлнэ."
            )

        st.divider()
        st.subheader("Q-System-ийн нийт үнэлгээ")
        st.write("Q = (RQD / Jn) × (Jr / Ja) × (Jw / SRF)")
        st.success(
            f"Q = {a:.3f} × {b:.3f} × {c:.3f} = {q_value:.3f}"
        )



elif menu == "Харьцуулалт":
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    st.header("RMR / GSI / Q-System харьцуулалт")
    st.write(
        "Чулуулгийн массивын чанарыг гурван өөр "
        "үнэлгээний аргаар нэгтгэн харуулсан үр дүн."
    )

    # Үр дүнгийн хүснэгт
    st.subheader("Үнэлгээний нэгдсэн үр дүн")

    rows = []

    if "final_rmr" in st.session_state:
        rows.append({
            "Үнэлгээний арга": "RMR",
            "Үр дүн": f'{st.session_state["final_rmr"]}/100',
            "Ангилал": st.session_state["rock_class"]
        })

    if "gsi_average" in st.session_state:
        rows.append({
            "Үнэлгээний арга": "GSI",
            "Үр дүн": (
                f'{st.session_state["gsi_min"]}–'
                f'{st.session_state["gsi_max"]} '
                f'(дундаж {st.session_state["gsi_average"]:.1f})'
            ),
            "Ангилал": "GSI индекс"
        })

    if "q_value" in st.session_state:
        rows.append({
            "Үнэлгээний арга": "Q-System",
            "Үр дүн": f'{st.session_state["q_value"]:.3f}',
            "Ангилал": st.session_state["q_class"]
        })

    if rows:
        st.dataframe(
            pd.DataFrame(rows),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.warning(
            "Эхлээд RMR, GSI, Q-System хэсгүүдэд үнэлгээ хийнэ үү."
        )

    st.divider()

    # Үр дүнгийн картууд
    st.subheader("Үнэлгээний үзүүлэлтүүд")

    col1, col2, col3 = st.columns(3)

    with col1:
        if "final_rmr" in st.session_state:
            st.metric(
                "RMR оноо",
                f'{st.session_state["final_rmr"]}/100',
                border=True
            )
        else:
            st.metric("RMR оноо", "Тооцоолоогүй", border=True)

    with col2:
        if "gsi_average" in st.session_state:
            st.metric(
                "GSI дундаж",
                f'{st.session_state["gsi_average"]:.1f}',
                border=True
            )
        else:
            st.metric("GSI дундаж", "Тооцоолоогүй", border=True)

    with col3:
        if "q_value" in st.session_state:
            st.metric(
                "Q-System утга",
                f'{st.session_state["q_value"]:.3f}',
                border=True
            )
        else:
            st.metric("Q-System утга", "Тооцоолоогүй", border=True)

    st.divider()

    # Интерактив график
    st.subheader("Үнэлгээний график харьцуулалт")

    fig = make_subplots(
        rows=1,
        cols=3,
        subplot_titles=(
            "RMR үнэлгээ",
            "GSI үнэлгээ",
            "Q-System үнэлгээ"
        ),
        horizontal_spacing=0.12
    )

    # RMR график
    if "final_rmr" in st.session_state:
        rmr = float(st.session_state["final_rmr"])

        fig.add_trace(
            go.Bar(
                x=["RMR"],
                y=[rmr],
                marker_color="#3B82F6",
                text=[f"{rmr:.1f}"],
                textposition="outside",
                name="RMR",
                showlegend=False
            ),
            row=1,
            col=1
        )

    # GSI график
    if "gsi_average" in st.session_state:
        gsi_min = float(st.session_state["gsi_min"])
        gsi_avg = float(st.session_state["gsi_average"])
        gsi_max = float(st.session_state["gsi_max"])

        fig.add_trace(
            go.Bar(
                x=["GSI"],
                y=[gsi_avg],
                marker_color="#10B981",
                text=[f"{gsi_avg:.1f}"],
                textposition="outside",
                error_y=dict(
                    type="data",
                    symmetric=False,
                    array=[gsi_max - gsi_avg],
                    arrayminus=[gsi_avg - gsi_min],
                    visible=True,
                    color="#047857",
                    thickness=2,
                    width=7
                ),
                name="GSI",
                showlegend=False
            ),
            row=1,
            col=2
        )

    # Q-System график
    if "q_value" in st.session_state:
        q = float(st.session_state["q_value"])

        fig.add_trace(
            go.Bar(
                x=["Q-System"],
                y=[q],
                marker_color="#F59E0B",
                text=[f"{q:.3f}"],
                textposition="outside",
                name="Q-System",
                showlegend=False
            ),
            row=1,
            col=3
        )

    # Графики тус бүрийн масштаб
    fig.update_yaxes(
        title_text="Оноо",
        range=[0, 100],
        row=1,
        col=1
    )

    fig.update_yaxes(
        title_text="GSI индекс",
        range=[0, 100],
        row=1,
        col=2
    )

    if "q_value" in st.session_state:
        q = float(st.session_state["q_value"])
        fig.update_yaxes(
            title_text="Q утга",
            range=[0, max(q * 1.25, 1)],
            row=1,
            col=3
        )

    fig.update_layout(
        template="plotly_white",
        height=430,
        showlegend=False,
        margin=dict(l=35, r=25, t=80, b=50),
        font=dict(
            family="Arial",
            size=13,
            color="#334155"
        ),
        bargap=0.55
    )

    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(
        gridcolor="#E2E8F0",
        zerolinecolor="#CBD5E1"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.caption(
        "Тайлбар: GSI графикийн босоо шугам нь доод болон "
        "дээд үнэлгээний мужийг илэрхийлнэ."
    )

    st.info(
        "Анхаарах нь: RMR, GSI болон Q-System нь өөр өөр "
        "масштаб, тооцооллын зарчимтай. Иймээс графикуудыг "
        "тус тусын масштабаар дүрсэлсэн бөгөөд оноог шууд "
        "хооронд нь харьцуулахгүй."
    )




