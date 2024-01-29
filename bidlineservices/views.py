from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from langchain.text_splitter import RecursiveCharacterTextSplitter

# from .models import Project, Tasks
# from .forms import CreateNewTask, CreateNewProject

# Create your views here.
def index(request):
  return HttpResponse(f'<h1>Welcome to Bidline Services</h1>')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({"message": "This is a protected view."})

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
def bid_slice_text(request, text):
  print(text)
  class Document:
    def __init__(self, content, metadata={}):
        self.page_content = content
        self.metadata = metadata

  def slice_text(documents, chunk_overlap=0, separators=["\n\n", "\n", "(?<=\. )", " "]):
    text_splitter = RecursiveCharacterTextSplitter(
        #chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=separators,
        length_function=len
    )
    return text_splitter.split_documents(documents)

  # Create a Document instance with your dummy text
  text = """
    REQUEST FOR PROPOSALS COMMUNICATIONS CONSULTING SERVICES
    I. GENERAL INFORMATION
    A. INTRODUCTION
    The Intergovernmental Personnel Benefit Cooperative (IPBC) is seeking proposals from
    qualified individuals or firms to provide communications consulting services for the
    IPBC. Successful applicants will demonstrate an ability to provide: provide a
    comprehensive analysis of IPBC’s communication structure and recommendation for a
    future state.
    B. BACKGROUND
    IPBC is a partnership of local government entities in Illinois that are committed to the
    philosophy of risk pooling and working together to provide cost-effective health and
    related employee benefits. Formed in 1979, IPBC has grown from 8 members to over
    160. It is open to municipalities, counties, special agencies, and intergovernmental
    organizations.
    IPBC is staffed by four (4) full-time staff members and one (1) part-time staff member.
    IPBC contracts with Risk Program Administrators (RPA) to provide benefit consulting
    services to the membership. RPA is currently staffed by ten (10) full-time staff members.
    IPBC provides health (BCBSIL, UHC), life (Securian), dental (DDIL), vision (VSP), and
    spending account (WEX) benefits for its membership. In addition, IPBC utilizes
    PlanSource as the benefits administration platform.
    IPBC communicates with its member entities who then are responsible for
    communicating their benefit programs with their employees. IPBC communicates with
    its members via:
    • Monthly Newsletter (Attachment A)
    • E-mail Blasts (Attachment B)
    • Governance Meetings – held quarterly, open to entire membership (Attachment
    C)
    • IPBC Website: [www.ipbchealth.org](http://www.ipbchealth.org/) – each member is given a login. The website
    contains information that is applicable to entire membership (financial reports,
    meeting packets, carrier flyers). The website does not have the ability to easily
    share/store member specific documents/information with the member entities.
    A quick video overview of the website is available here:
    https://vimeo.com/manage/videos/888761301
    • Individual communications between IPBC and benefit consultants via e-mail and
    phone.
    IPBC member entities are responsible for communicating their individual benefits
    program(s) to their employees. It is at the discretion of the member entities on how they
    communicate with their employees (i.e, email, intranet, employer newsletters etc.) In
    addition, IPBC carrier partners communicate directly with employees on their services.
    C. ANTICIPATED SELECTION SCHEDULE
    IPBC anticipates the following general timeline for its selection process. The IPBC
    reserves the right to change this schedule.
    • RFP Advertised Week of November 27, 2023
    • Proposal Due Date (post marked by) December 20, 2023 by 5:00 pm
    • Evaluation of Proposals Weel of January 8, 2024
    • Interviews (if needed) Week of January 29, 2024
    • Contract Approval March 2024 (Board Meeting)
    • Commencement of Contract July 1, 2024
    D. SCOPE OF SERVICES
    The scope of work will include the following tasks:
    Development of a Communications Plan for IPBC, which should include coordination with
    the IPBC Staff and the IPBC Membership Development Committee on both planning and
    implementation.
    Creation/recommendation of the necessary infrastructure, such as websites or other
    communications tools, to enable plan implementation to begin, and support for
    implementation of the approved communications plan during the initial 6-12 months. This
    may include, but not be limited to:
     Conducting an Inventory of all current communication materials
     Coordinating the communication strategies with IPBC Staff and the
    Membership Development Committee,
     Producing creative materials and building/recommending the necessary
    dissemination infrastructure,
     Writing articles, marketing pieces, information releases,
    Primary Audience
    The primary audience is Human Resources and Finance staff of local government agencies
    who are responsible for managing their entity’s benefit program(s). The secondary
    audience are the employees who are participating in an IPBC benefit program.
    Anticipated Contract Type
    IPBC would expect to negotiate a firm fixed fee and enter into a contract for
    communications service(s) selected through this RFP. This contract is expected to have a
    duration of 18-24 months, depending upon the length of the Task 1 planning phase and the
    activities subsequently agreed upon for future phases. The contract may be renewed,
    based upon performance and need.
    II. PROPOSAL INSTRUCTIONS
    A. PROPOSAL SUBMITTAL AND DUE DATE
    Proposers shall provide proposal electronically marked “IPBC Communications Services
    Proposal”. Proposals shall be submitted by 5:00 p.m. on XX to:
    Sandy Mikel
    Member Services Manager
    [smikel@ipbchealth.org](mailto:smikel@ipbchealth.org)
    B. INQUIRIES
    Questions concerning this RFP should be submitted to:
    Sandy Mikel
    Member Services Manager
    [smikel@ipbchealth.org](mailto:smikel@ipbchealth.org)
    IPBC will not respond to questions received after 3:00p.m. on December 20, 2023.
    C. RESERVATION OF RIGHTS
    IPBC reserves the right to: 1) seek clarifications of each proposal; 2) negotiate a final
    contract that is in the best interest of the IPBC and its membership; 3) reject any or all
    proposals; 4) cancel this RFP at any time if doing so would be in the membership’s
    interest, as determined by IPBC in its sole discretion; 5) award the contract to any
    proposer based on the evaluation criteria set forth in this RFP; 6) waive minor informalities
    contained in any proposal, when, in the IPBC’s sole judgment, it is in the IPBC’s best
    interest to do so; and 7) request any additional information IPBC deems reasonably
    necessary to allow IPBC to evaluate, rank and select the most qualified Proposer to
    perform the services described in this RFP.
    D. PROPOSAL CONTENTS
    Proposals shall include, at a minimum, the following items:
    - Cover Letter. A one page cover letter containing:
    * the name of the person(s) authorized to represent the Proposer
    in negotiating and signing any agreement which may result from the
    proposal;
    * Entity name and address;
    * Phone, website and email address; and
    - Staffing. Name and qualifications of the individuals who will provide the requested
    services and a current résumé for each, including a description of qualifications,
    skills, and responsibilities. The IPBC is interested in professionals with experience
    serving governmental entities and membership organizations comparable to IPBC.
    - Approach/Work Plan. Describe how the Proposer approaches marketing and
    communications projects. How do you assist clients in using existing resources and
    leveraging the work you provide for them?
    - Experience/Work Samples. Provide previous work examples that demonstrate how
    you meet the experience requirements listed in this RFP. Submit three projects
    undertaken in the past three years (preferably for a membership organization
    similar to in structure to IPBC)
    - Cost/Budget. Provide hourly rates or other fee structures for the services listed in
    Article 1.E, Scope of Services, of this RFP.
    - Capacity. Explain proposer’s workload capacity and level of
    experience commensurate with the level of service required by IPBC.
    - Insurance. Proof of Insurance of $2 million comprehensive and automobile liability
    insurance, as well as proof of coverage by Workers’ Compensation Insurance or
    exemption.
    - Subconsultants. A list of the tasks, responsibilities, and qualifications of any
    subconsultants proposed to be used on a routine basis.
    - Nondiscrimination. Written affirmation that the firm has a policy of
    nondiscrimination in employment because of race, age, color, sex, religion, national
    origin, mental or physical handicap, political affiliation, marital status or other
    protected class, and has a drug-free workplace policy.
    E. INFORMATION RELEASE
    Proposers are hereby advised that IPBC may solicit background information based upon
    all information, including references, provided in response to this RFP. By submission of
    a proposal, Proposer agrees to such activity and releases IPBC from all claims arising
    from such activity.
    F. PUBLIC RECORDS
    All proposals submitted are the property of IPBC, and are thus subject to disclosure
    pursuant to the public records law.
    Proposers responding to this RFP do so solely at their own expense.
    III. PROPOSAL EVALUATION
    A. MINIMUM QUALIFICATIONS
    The IPBC will review proposals received to determine whether or not each proposer
    meets the following minimum qualifications:
    • Ability to provide the marketing and communications services work needed by
    the IPBC to the standards required by the IPBC.
    • Has the financial resources for the performance of the desired marketing and
    communication services, or the ability to obtain such resources.
    • Is an Equal Opportunity Employer and otherwise qualified by law to enter into the
    attached Marketing and Communications Services Contract.
    B. EVALUATION CRITERIA
    If an award is made, it is expected that the IPBC’s award will be to the applicant that agrees
    to meet the needs of the IPBC. A number of relevant matters will be considered, including:
    1. Experience in the development of communications plans of similar purpose and
    scope
    2. Demonstrated effectiveness in the implementation of a variety of communications
    tactics that achieve established goals
    3. Understanding of and approach to the listed scope of services
    4. Cost proposal
    Interviews may be requested prior to final selection.
    C. SELECTION
    An evaluation committee will evaluate all proposals. The committee will be composed of
    IPBC Staff, Benefit Consulting Staff and members of the IPBC Membership Development
    Committee.
    Upon completion of its evaluation process, the evaluation committee shall provide the
    results of the scoring and ranking to the IPBC Board of Directors, along with a
    recommendation to award the contract to the highest ranked Proposer.
    D. CONTRACT
    IPBC desires to enter into a professional services agreement, which includes all necessary
    marketing and communications services, whether or not the services are specifically
    outlined in this RFP. The agreement requires that awardee comply with all applicable
    federal and state laws, rules and regulations
    IPBC is an Equal Opportunity/Affirmative Action Employer. Women,
    Minorities, and Disabled Persons are encouraged to apply.
    THIS SOLICITATION IS NOT AN IMPLIED CONTRACT AND MAY BE
    MODIFIED OR REVOKED WITHOUT NOTICE.
  """
  data = Document(text)
  
  # Slicing the dummy text
  sliced_docs = slice_text([data])
  slice_output = []
  length_of_sliced_docs = len(sliced_docs)

  for i, doc in enumerate(sliced_docs):
    document_object = {
      "contect" : doc.page_content,
      "part_number" : i
    }

    slice_output.append(document_object)

  final_output = json.dumps(slice_output, indent = 4)

  return JsonResponse(final_output, safe=False)

# @api_view(['GET'])
def unprotected_view(request):
    return HttpResponse(f'<h1>Welcome to Bidline Services</h1>')
