import streamlit as st
import pandas as pd
import plotly.express as px
import uuid
from datetime import datetime, timedelta

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="GrabZy",
    page_icon="🚀",
    layout="wide"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

[data-testid="stMetric"]{
    background-color:#f8f9fa;
    padding:15px;
    border-radius:12px;
    border:1px solid #dddddd;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# SESSION STATE INITIALIZATION
# =====================================================

if "students" not in st.session_state:
    st.session_state.students = []

if "resources" not in st.session_state:

    st.session_state.resources = [

        {
            "item": "Scientific Calculator",
            "category": "Academic",
            "available": 15,
            "price": 10,
            "item_cost": 500,
            "condition": "Good"
        },

        {
            "item": "Umbrella",
            "category": "Emergency",
            "available": 10,
            "price": 5,
            "item_cost": 300,
            "condition": "Good"
        },

        {
            "item": "Laptop Charger",
            "category": "Electronics",
            "available": 8,
            "price": 15,
            "item_cost": 800,
            "condition": "Good"
        },

        {
            "item": "Lab Coat",
            "category": "Lab Equipment",
            "available": 12,
            "price": 20,
            "item_cost": 1000,
            "condition": "Good"
        }

    ]

if "rentals" not in st.session_state:
    st.session_state.rentals = []

if "notifications" not in st.session_state:
    st.session_state.notifications = []

if "sanitation" not in st.session_state:
    st.session_state.sanitation = []

if "cart" not in st.session_state:
    st.session_state.cart = []

if "student_logged_in" not in st.session_state:
    st.session_state.student_logged_in = False

if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

if "current_student" not in st.session_state:
    st.session_state.current_student = ""

# =====================================================
# HELPER FUNCTIONS
# =====================================================

def add_notification(student, message):

    st.session_state.notifications.append(
        {
            "student": student,
            "message": message,
            "time": str(datetime.now())
        }
    )

# =====================================================
# APP HEADER
# =====================================================

st.title("🚀 GrabZy")

st.caption(
    "Smart Campus Resource Rental System"
)

role = st.sidebar.selectbox(
    "Select Role",
    [
        "Student",
        "Admin"
    ]
)

# =====================================================
# STUDENT MODULE
# =====================================================

if role == "Student":

    # -------------------------------------------------
    # LOGIN / SIGNUP
    # -------------------------------------------------

    if not st.session_state.student_logged_in:

        option = st.radio(
            "Choose Option",
            [
                "Login",
                "Create Account"
            ]
        )

        # ---------------------------------------------
        # CREATE ACCOUNT
        # ---------------------------------------------

        if option == "Create Account":

            st.subheader(
                "Create Student Account"
            )

            student_name = st.text_input(
                "Student Name"
            )

            roll_number = st.text_input(
                "Roll Number"
            )

            email = st.text_input(
                "Email"
            )

            password = st.text_input(
                "Password",
                type="password"
            )

            if st.button(
                "Create Account"
            ):

                st.session_state.students.append(
                    {
                        "name": student_name,
                        "roll": roll_number,
                        "email": email,
                        "password": password
                    }
                )

                st.success(
                    "Account Created Successfully"
                )

        # ---------------------------------------------
        # LOGIN
        # ---------------------------------------------

        else:

            st.subheader(
                "Student Login"
            )

            roll_number = st.text_input(
                "Roll Number"
            )

            email = st.text_input(
                "Email"
            )

            password = st.text_input(
                "Password",
                type="password"
            )

            if st.button(
                "Login"
            ):

                st.session_state.student_logged_in = True

                st.session_state.current_student = email

                st.success(
                    "Login Successful"
                )

                st.rerun()

    # -------------------------------------------------
    # STUDENT LOGGED IN
    # -------------------------------------------------

    else:

        if st.sidebar.button(
            "🚪 Sign Out"
        ):

            st.session_state.student_logged_in = False

            st.session_state.current_student = ""

            st.session_state.cart = []

            st.rerun()

        student_menu = st.sidebar.radio(
            "Student Menu",
            [
                "Dashboard",
                "Resource Catalog",
                "Cart",
                "My Rentals",
                "Notifications",
                "Return Resource"
            ]
        )
        # =====================================================
        # DASHBOARD
        # =====================================================

        if student_menu == "Dashboard":

            active_rentals = 0
            due_soon = 0

            for rental in st.session_state.rentals:

                if (
                    rental["student"]
                    == st.session_state.current_student
                    and rental["status"] == "Active"
                ):

                    active_rentals += 1

                    days_left = (
                        rental["due_date"]
                        - datetime.now().date()
                    ).days

                    if days_left <= 2:
                        due_soon += 1

            st.subheader(
                f"Welcome, {st.session_state.current_student}"
            )

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Total Available Resources",
                sum(
                    item["available"]
                    for item in st.session_state.resources
                )
            )

            col2.metric(
                "My Active Rentals",
                active_rentals
            )

            col3.metric(
                "Due Soon Items",
                due_soon
            )

            st.divider()

            search_text = st.text_input(
                "🔍 Search Resources"
            )

            if search_text:

                results = []

                for resource in st.session_state.resources:

                    if (
                        search_text.lower()
                        in resource["item"].lower()
                    ):
                        results.append(resource)

                if len(results) > 0:

                    st.dataframe(
                        pd.DataFrame(results)
                    )

                else:

                    st.warning(
                        "No matching resources found."
                    )

        # =====================================================
        # RESOURCE CATALOG
        # =====================================================

        elif student_menu == "Resource Catalog":

            st.subheader(
                "📚 Resource Catalog"
            )

            resources_df = pd.DataFrame(
                st.session_state.resources
            )

            category = st.selectbox(
                "Select Category",
                [
                    "All",
                    "Academic",
                    "Electronics",
                    "Lab Equipment",
                    "Emergency"
                ]
            )

            if category != "All":

                resources_df = resources_df[
                    resources_df["category"]
                    == category
                ]

            st.dataframe(
                resources_df,
                use_container_width=True
            )

            st.divider()

            selected_item = st.selectbox(
                "Choose Resource",
                resources_df["item"]
            )

            selected_resource = resources_df[
                resources_df["item"]
                == selected_item
            ].iloc[0]

            st.subheader(
                "Resource Details"
            )

            st.write(
                f"**Item Name:** {selected_resource['item']}"
            )

            st.write(
                f"**Category:** {selected_resource['category']}"
            )

            st.write(
                f"**Available Quantity:** {selected_resource['available']}"
            )

            st.write(
                f"**Rental Price:** ₹{selected_resource['price']} / day"
            )

            st.write(
                f"**Condition:** {selected_resource['condition']}"
            )

            st.write(
                "**Penalty:** ₹30/day after due date"
            )

            st.write(
                "After 10 days overdue, full item cost is charged."
            )

            quantity = st.number_input(
                "Quantity",
                min_value=1,
                max_value=max(
                    1,
                    int(selected_resource["available"])
                ),
                value=1
            )

            rental_days = st.number_input(
                "Rental Duration (Days)",
                min_value=1,
                max_value=30,
                value=1
            )

            rental_cost = (
                quantity
                * rental_days
                * selected_resource["price"]
            )

            st.success(
                f"Rental Cost: ₹{rental_cost}"
            )

            if st.button(
                "Add To Cart"
            ):

                st.session_state.cart.append(
                    {
                        "item": selected_resource["item"],
                        "quantity": quantity,
                        "days": rental_days,
                        "amount": rental_cost
                    }
                )

                st.success(
                    "Resource Added To Cart"
                )
        # =====================================================
        # CART
        # =====================================================

        elif student_menu == "Cart":

            st.subheader("🛒 My Cart")

            if len(st.session_state.cart) == 0:

                st.info(
                    "Your cart is empty."
                )

            else:

                cart_df = pd.DataFrame(
                    st.session_state.cart
                )

                st.dataframe(
                    cart_df,
                    use_container_width=True
                )

                total_amount = (
                    cart_df["amount"].sum()
                )

                st.subheader(
                    f"Total Amount: ₹{total_amount}"
                )

                pickup_center = st.selectbox(
                    "Select Pickup Resource Centre",
                    [
                        "Main Library",
                        "Engineering Block",
                        "Student Activity Centre",
                        "Hostel Resource Hub"
                    ]
                )

                payment_method = st.selectbox(
                    "Payment Method",
                    [
                        "UPI",
                        "Card",
                        "Cash"
                    ]
                )

                if st.button(
                    "Checkout"
                ):

                    rental_code = (
                        "SCRS"
                        + str(uuid.uuid4().int)[:6]
                    )

                    start_date = (
                        datetime.now().date()
                    )

                    for item in st.session_state.cart:

                        due_date = (
                            start_date
                            + timedelta(
                                days=item["days"]
                            )
                        )

                        st.session_state.rentals.append(
                            {
                                "rental_code": rental_code,
                                "student": st.session_state.current_student,
                                "item": item["item"],
                                "quantity": item["quantity"],
                                "start_date": start_date,
                                "due_date": due_date,
                                "amount": item["amount"],
                                "status": "Active",
                                "penalty": 0
                            }
                        )

                        for resource in st.session_state.resources:

                            if (
                                resource["item"]
                                == item["item"]
                            ):

                                resource["available"] -= (
                                    item["quantity"]
                                )

                    add_notification(
                        st.session_state.current_student,
                        f"Rental Confirmed ({rental_code})"
                    )

                    st.session_state.cart = []

                    st.balloons()

                    st.success(
                        f"""
                        Payment Successful

                        Rental Code:
                        {rental_code}
                        """
                    )

                    st.info(
                        f"""
                        Please collect your
                        resource from:

                        📍 {pickup_center}

                        Share Rental Code:

                        {rental_code}
                        """
                    )

        # =====================================================
        # MY RENTALS
        # =====================================================

        elif student_menu == "My Rentals":

            st.subheader(
                "📦 My Rentals"
            )

            my_rentals = []

            for rental in st.session_state.rentals:

                if (
                    rental["student"]
                    == st.session_state.current_student
                ):

                    my_rentals.append(
                        rental
                    )

            if len(my_rentals) == 0:

                st.info(
                    "No rentals found."
                )

            else:

                st.dataframe(
                    pd.DataFrame(my_rentals),
                    use_container_width=True
                )

        # =====================================================
        # NOTIFICATIONS
        # =====================================================

        elif student_menu == "Notifications":

            st.subheader(
                "🔔 Notifications"
            )

            student_notifications = []

            for notification in (
                st.session_state.notifications
            ):

                if (
                    notification["student"]
                    == st.session_state.current_student
                ):

                    student_notifications.append(
                        notification
                    )

            if len(student_notifications) == 0:

                st.info(
                    "No notifications."
                )

            else:

                notifications_df = pd.DataFrame(
                    student_notifications
                )

                st.dataframe(
                    notifications_df,
                    use_container_width=True
                )
        # =====================================================
        # RETURN RESOURCE
        # =====================================================

        elif student_menu == "Return Resource":

            st.subheader(
                "↩ Return Resource"
            )

            active_rentals = []

            for rental in st.session_state.rentals:

                if (
                    rental["student"]
                    == st.session_state.current_student
                    and rental["status"] == "Active"
                ):

                    active_rentals.append(
                        rental
                    )

            if len(active_rentals) == 0:

                st.info(
                    "No Active Rentals Found"
                )

            else:

                rental_options = []

                for rental in active_rentals:

                    rental_options.append(
                        f"{rental['rental_code']} - {rental['item']}"
                    )

                selected_option = st.selectbox(
                    "Select Rental",
                    rental_options
                )

                selected_rental = None

                for rental in active_rentals:

                    option_text = (
                        f"{rental['rental_code']} - {rental['item']}"
                    )

                    if option_text == selected_option:

                        selected_rental = rental
                        break

                st.write(
                    f"**Rental Code:** {selected_rental['rental_code']}"
                )

                st.write(
                    f"**Item:** {selected_rental['item']}"
                )

                st.write(
                    f"**Borrow Date:** {selected_rental['start_date']}"
                )

                st.write(
                    f"**Due Date:** {selected_rental['due_date']}"
                )

                return_date = datetime.now().date()

                late_days = (
                    return_date
                    - selected_rental["due_date"]
                ).days

                if late_days < 0:
                    late_days = 0

                penalty = late_days * 30

                if late_days > 10:

                    for resource in st.session_state.resources:

                        if (
                            resource["item"]
                            == selected_rental["item"]
                        ):

                            penalty = (
                                resource["item_cost"]
                            )

                            break

                st.write(
                    f"**Late Days:** {late_days}"
                )

                st.write(
                    f"**Penalty Amount:** ₹{penalty}"
                )

                if st.button(
                    "Complete Return"
                ):

                    selected_rental["status"] = (
                        "Returned"
                    )

                    selected_rental["penalty"] = (
                        penalty
                    )

                    st.session_state.sanitation.append(
                        {
                            "item":
                            selected_rental["item"],

                            "return_date":
                            str(return_date),

                            "status":
                            "Needs Cleaning"
                        }
                    )

                    add_notification(
                        st.session_state.current_student,
                        f"""
                        Return Completed
                        ({selected_rental['rental_code']})
                        """
                    )

                    st.balloons()

                    st.success(
                        "Return Recorded Successfully"
                    )

                    st.info(
                        f"""
                        Please return the resource
                        at the nearest Resource Centre.

                        Rental Code:
                        {selected_rental['rental_code']}
                        """
                    )
# =====================================================
# ADMIN MODULE
# =====================================================

elif role == "Admin":

    # -------------------------------------------------
    # ADMIN LOGIN
    # -------------------------------------------------

    if not st.session_state.admin_logged_in:

        st.subheader(
            "👨‍💼 Admin Login"
        )

        admin_email = st.text_input(
            "Admin Email"
        )

        admin_password = st.text_input(
            "Password",
            type="password"
        )

        if st.button(
            "Admin Login"
        ):

            st.session_state.admin_logged_in = True

            st.success(
                "Admin Login Successful"
            )

            st.rerun()

    # -------------------------------------------------
    # ADMIN LOGGED IN
    # -------------------------------------------------

    else:

        if st.sidebar.button(
            "🚪 Admin Sign Out"
        ):

            st.session_state.admin_logged_in = False

            st.rerun()

        admin_menu = st.sidebar.radio(
            "Admin Menu",
            [
                "Dashboard",
                "Inventory",
                "Penalty Dashboard",
                "Sanitation Dashboard",
                "Damaged Items"
            ]
        )

        # =================================================
        # DASHBOARD
        # =================================================

        if admin_menu == "Dashboard":

            resources_df = pd.DataFrame(
                st.session_state.resources
            )

            rentals_df = pd.DataFrame(
                st.session_state.rentals
            )

            total_resources = len(
                resources_df
            )

            available_resources = 0

            if len(resources_df) > 0:

                available_resources = (
                    resources_df["available"]
                    .sum()
                )

            active_rentals = 0

            for rental in st.session_state.rentals:

                if rental["status"] == "Active":

                    active_rentals += 1

            overdue_rentals = 0

            today = datetime.now().date()

            for rental in st.session_state.rentals:

                if (
                    rental["status"] == "Active"
                    and rental["due_date"] < today
                ):

                    overdue_rentals += 1

            total_revenue = 0

            for rental in st.session_state.rentals:

                total_revenue += rental["amount"]

            c1, c2, c3, c4, c5 = st.columns(5)

            c1.metric(
                "Total Resources",
                total_resources
            )

            c2.metric(
                "Available Resources",
                available_resources
            )

            c3.metric(
                "Currently Rented",
                active_rentals
            )

            c4.metric(
                "Overdue Rentals",
                overdue_rentals
            )

            c5.metric(
                "Revenue",
                f"₹{total_revenue}"
            )

            st.divider()

            st.subheader(
                "📊 Rental Analytics"
            )

            if len(rentals_df) > 0:

                rental_counts = (
                    rentals_df
                    .groupby("item")
                    .size()
                    .reset_index(
                        name="Rentals"
                    )
                )

                fig1 = px.bar(
                    rental_counts,
                    x="item",
                    y="Rentals",
                    title="Most Rented Items"
                )

                st.plotly_chart(
                    fig1,
                    use_container_width=True
                )

                category_data = []

                for resource in (
                    st.session_state.resources
                ):

                    count = 0

                    for rental in (
                        st.session_state.rentals
                    ):

                        if (
                            rental["item"]
                            == resource["item"]
                        ):

                            count += 1

                    category_data.append(
                        {
                            "Category":
                            resource["category"],

                            "Count":
                            count
                        }
                    )

                category_df = pd.DataFrame(
                    category_data
                )

                if len(category_df) > 0:

                    category_summary = (
                        category_df
                        .groupby("Category")
                        ["Count"]
                        .sum()
                        .reset_index()
                    )

                    fig2 = px.pie(
                        category_summary,
                        names="Category",
                        values="Count",
                        title="Category Wise Rentals"
                    )

                    st.plotly_chart(
                        fig2,
                        use_container_width=True
                    )

                st.subheader(
                    "Rental Records"
                )

                st.dataframe(
                    rentals_df,
                    use_container_width=True
                )

            else:

                st.info(
                    "No rentals available yet."
                )
        # =================================================
        # INVENTORY MANAGEMENT
        # =================================================

        elif admin_menu == "Inventory":

            st.subheader(
                "📦 Inventory Management"
            )

            resources_df = pd.DataFrame(
                st.session_state.resources
            )

            st.dataframe(
                resources_df,
                use_container_width=True
            )

            st.divider()

            st.subheader(
                "Add New Resource"
            )

            with st.form("add_resource_form"):

                item_name = st.text_input(
                    "Item Name"
                )

                category = st.selectbox(
                    "Category",
                    [
                        "Academic",
                        "Electronics",
                        "Lab Equipment",
                        "Emergency"
                    ]
                )

                quantity = st.number_input(
                    "Quantity",
                    min_value=1,
                    value=1
                )

                rental_price = st.number_input(
                    "Rental Price Per Day",
                    min_value=1,
                    value=10
                )

                item_cost = st.number_input(
                    "Full Item Cost",
                    min_value=100,
                    value=500
                )

                condition = st.selectbox(
                    "Condition",
                    [
                        "Good",
                        "Fair",
                        "Damaged"
                    ]
                )

                submitted = st.form_submit_button(
                    "Add Resource"
                )

                if submitted:

                    st.session_state.resources.append(
                        {
                            "item": item_name,
                            "category": category,
                            "available": quantity,
                            "price": rental_price,
                            "item_cost": item_cost,
                            "condition": condition
                        }
                    )

                    st.success(
                        "Resource Added Successfully"
                    )

            st.divider()

            st.subheader(
                "Edit Resource"
            )

            if len(st.session_state.resources) > 0:

                resource_names = [
                    resource["item"]
                    for resource in st.session_state.resources
                ]

                selected_resource = st.selectbox(
                    "Select Resource",
                    resource_names
                )

                resource = next(
                    r for r in st.session_state.resources
                    if r["item"] == selected_resource
                )

                new_available = st.number_input(
                    "Available Quantity",
                    min_value=0,
                    value=int(resource["available"])
                )

                new_price = st.number_input(
                    "Rental Price",
                    min_value=1,
                    value=int(resource["price"])
                )

                new_condition = st.selectbox(
                    "Condition",
                    [
                        "Good",
                        "Fair",
                        "Damaged"
                    ]
                )

                if st.button(
                    "Update Resource"
                ):

                    resource["available"] = (
                        new_available
                    )

                    resource["price"] = (
                        new_price
                    )

                    resource["condition"] = (
                        new_condition
                    )

                    st.success(
                        "Resource Updated"
                    )

            st.divider()

            st.subheader(
                "Delete Resource"
            )

            if len(st.session_state.resources) > 0:

                delete_item = st.selectbox(
                    "Select Resource To Delete",
                    [
                        resource["item"]
                        for resource
                        in st.session_state.resources
                    ],
                    key="delete_resource"
                )

                if st.button(
                    "Delete Resource"
                ):

                    st.session_state.resources = [

                        resource

                        for resource
                        in st.session_state.resources

                        if resource["item"]
                        != delete_item
                    ]

                    st.success(
                        "Resource Deleted"
                    )

        # =================================================
        # PENALTY DASHBOARD
        # =================================================

        elif admin_menu == "Penalty Dashboard":

            st.subheader(
                "⚠ Penalty Dashboard"
            )

            penalties = []

            for rental in st.session_state.rentals:

                if rental["penalty"] > 0:

                    penalties.append(
                        rental
                    )

            if len(penalties) == 0:

                st.info(
                    "No Penalties Recorded"
                )

            else:

                st.dataframe(
                    pd.DataFrame(penalties),
                    use_container_width=True
                )

                total_penalty = sum(
                    item["penalty"]
                    for item in penalties
                )

                st.metric(
                    "Total Penalties",
                    f"₹{total_penalty}"
                )

        # =================================================
        # SANITATION DASHBOARD
        # =================================================

        elif admin_menu == "Sanitation Dashboard":

            st.subheader(
                "🧼 Sanitation Dashboard"
            )

            sanitation_df = pd.DataFrame(
                st.session_state.sanitation
            )

            if len(sanitation_df) == 0:

                st.info(
                    "No Items Awaiting Cleaning"
                )

            else:

                st.dataframe(
                    sanitation_df,
                    use_container_width=True
                )

                pending = len(
                    sanitation_df[
                        sanitation_df["status"]
                        == "Needs Cleaning"
                    ]
                )

                st.metric(
                    "Pending Cleaning",
                    pending
                )

                item_to_clean = st.selectbox(
                    "Select Item",
                    sanitation_df["item"]
                )

                if st.button(
                    "Mark Sanitized"
                ):

                    for item in (
                        st.session_state.sanitation
                    ):

                        if (
                            item["item"]
                            == item_to_clean
                        ):

                            item["status"] = (
                                "Sanitized"
                            )

                    for resource in (
                        st.session_state.resources
                    ):

                        if (
                            resource["item"]
                            == item_to_clean
                        ):

                            resource["available"] += 1

                    st.success(
                        "Item Sanitized & Available"
                    )

        # =================================================
        # DAMAGED ITEMS
        # =================================================

        elif admin_menu == "Damaged Items":

            st.subheader(
                "🔧 Damaged Resources"
            )

            damaged_items = []

            for resource in (
                st.session_state.resources
            ):

                if (
                    resource["condition"]
                    == "Damaged"
                ):

                    damaged_items.append(
                        resource
                    )

            if len(damaged_items) == 0:

                st.success(
                    "No Damaged Resources"
                )

            else:

                st.dataframe(
                    pd.DataFrame(
                        damaged_items
                    ),
                    use_container_width=True
                )

                st.metric(
                    "Damaged Count",
                    len(damaged_items)
                )

            st.divider()

            st.subheader(
                "🛠 Update Borrowed Resource Condition"
            )

            active_borrowed = []

            for rental in st.session_state.rentals:

                if rental["status"] == "Active":

                    active_borrowed.append(
                        rental
                    )

            if len(active_borrowed) == 0:

                st.info(
                    "No currently borrowed resources available to update."
                )

            else:

                borrowed_options = [
                    f"{r['rental_code']} - {r['item']} ({r['student']})"
                    for r in active_borrowed
                ]

                selected_borrowed = st.selectbox(
                    "Select Borrowed Resource",
                    borrowed_options
                )

                selected_rental = None

                for rental in active_borrowed:

                    option_text = (
                        f"{rental['rental_code']} - {rental['item']} ({rental['student']})"
                    )

                    if option_text == selected_borrowed:

                        selected_rental = rental
                        break

                if selected_rental is not None:

                    status_choice = st.radio(
                        "Mark Resource As",
                        ["Damaged", "Not Damaged"]
                    )

                    if st.button(
                        "Update Damage Status"
                    ):

                        for resource in st.session_state.resources:

                            if (
                                resource["item"]
                                == selected_rental["item"]
                            ):

                                resource["condition"] = (
                                    "Damaged"
                                    if status_choice == "Damaged"
                                    else "Good"
                                )
                                break

                        selected_rental["damage_status"] = (
                            status_choice
                        )

                        add_notification(
                            selected_rental["student"],
                            f"Your borrowed item {selected_rental['item']} has been marked as {status_choice}."
                        )

                        st.success(
                            f"{selected_rental['item']} marked as {status_choice}."
                        )
      