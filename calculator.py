class BeamCalculator:
    def __init__(self):
        pass

    # Function to get user inputs
    def get_user_input(self):
        print("Enter beam details:")

        num_spans = int(input("Number of spans: "))
        lengths = []
        for i in range(num_spans):
            length = float(input(f"Length of span {i+1} (m): "))
            if length <= 0:
                raise ValueError("Span length must be greater than zero.")
            lengths.append(length)

        load_type = input("Type of load on the entire beam (uniformly distributed or point load): ")
        loads = []
        if load_type.lower() == "uniformly distributed":
            load_value = float(input("Load per unit length (N/m): "))
            if load_value <= 0:
                raise ValueError("Load must be greater than zero.")
            loads.append((load_value, 'uniform', None))
        elif load_type.lower() == "point load":
            load_value = float(input("Point load magnitude (N): "))
            position = float(input("Position of point load from start of the first span (m): "))
            if load_value <= 0 or position <= 0 or position > sum(lengths):
                raise ValueError("Invalid point load details.")
            loads.append((load_value, 'point', position))
        else:
            print("Invalid load type. Please enter either 'uniformly distributed' or 'point load'.")
            return None, None, None

        type_of_beam = input("Type of Beam: ")
        
        # Dictionary to store section types and their respective dimensions
        sections = {
            "circular": ("Pipe outer diameter (m): ", float, "Pipe thickness (mm): ", float),
            "I-type": ("Upper flange width (mm): ", float, "Upper flange thickness (mm): ", float,
                        "Lower flange width (mm): ", float, "Lower flange thickness (mm): ", float,
                        "Web height (mm): ", float, "Web thickness (mm): ", float),
            "Box profile": ("Box width (mm): ", float, "Box height (mm): ", float,
                            "Box thickness (mm): ", float),
            "Rectangular full section": ("Rectangle width (mm): ", float, "Rectangle height (mm): ", float)
        }

        if type_of_beam not in sections:
            print("Invalid beam type. Please select one of the available types.")
            return None

        # Get dimensions based on selected section type
        dimensions = []
        for dim_name, dim_type in sections[type_of_beam]:
            value = dim_type(input(f"{dim_name} "))
            dimensions.append((dim_name, value))

        results = self.calculate_for_continuous_beam(lengths, loads)

        return results, dimensions

    def calculate_for_continuous_beam(self, lengths, loads):
        # Placeholder for beam calculation logic
        results = []
        for length in lengths:
            # Example: Assuming a constant load distribution
            bending_moment = (1/8) * sum(load[0] * length**2 for load in loads)
            shear_force = sum(load[0] for load in loads)

            results.append({
                "Bending Moment (N*m)": bending_moment,
                "Shear Force (N)": shear_force
            })

        return results

    # Get section properties
    yield_stress = float(input("Yield Stress (MPa): ")) * 1e6
    moment_of_inertia = 0

if __name__ == "__main__":
    beam_calculator = BeamCalculator()
    try:
        results, dimensions = beam_calculator.get_user_input()

        for i, result in enumerate(results):
            print(f"Span {i+1}:")
            print("Bending Moment: ", result["Bending Moment (N*m)"], "N*m")
            print("Shear Force: ", result["Shear Force (N)"], "N\n")

        # Get section properties
        yield_stress = float(input("Yield Stress (MPa): ")) * 1e6
        moment_of_inertia = 0

        if dimensions[0][0] == "Pipe outer diameter":
            radius = dimensions[0][1] / 2
            thickness = dimensions[1][1] / 1000
            moment_of_inertia = (3.14159 / 4) * (radius**4 - (radius - thickness)**4)
        elif dimensions[0][0] == "Upper flange width":
            upper_flange_width = dimensions[0][1] / 1000
            upper_flange_thickness = dimensions[1][1] / 1000
            lower_flange_width = dimensions[2][1] / 1000
            lower_flange_thickness = dimensions[3][1] / 1000
            web_height = dimensions[4][1] / 1000
            web_thickness = dimensions[5][1] / 1000

        sections = {
            "yield_stress": yield_stress,
            "moment_of_inertia": moment_of_inertia
        }

        # Check section capacity and calculate displacements
        for i, result in enumerate(results):
            M_max = result["Bending Moment (N*m)"]
            
            if M_max > sections["yield_stress"] * sections["moment_of_inertia"]:
                print(f"Span {i + 1}: The section cannot carry the loads.")
            else:
                print(f"Span {i + 1}: The section can carry the loads.")

        displacements = beam_calculator.calculate_maximum_displacement_and_capacity([result["Bending Moment (N*m)"] for result in results], sections)
    
        if all(d < sections["yield_stress"] * sections["moment_of_inertia"] / 600 for d in displacements):
            print("All displacements are within allowable limits.")
        else:
            print("Some displacements exceed allowable limits.")

        print(f"For a {type_of_beam} of material with dimensions:")
        for dim_name, dim_value in dimensions:
            print(f"{dim_name}: {dim_value}")

    except ValueError as e:
        print(e)
