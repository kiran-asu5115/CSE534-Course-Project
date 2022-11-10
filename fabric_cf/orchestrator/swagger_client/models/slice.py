# coding: utf-8

"""
    Fabric Orchestrator API

    This is Fabric Orchestrator API  # noqa: E501

    OpenAPI spec version: 1.0.1
    Contact: kthare10@unc.edu
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class Slice(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'model': 'str',
        'lease_start_time': 'str',
        'lease_end_time': 'str',
        'state': 'str',
        'project_id': 'str',
        'graph_id': 'str',
        'name': 'str',
        'slice_id': 'str'
    }

    attribute_map = {
        'model': 'model',
        'lease_start_time': 'lease_start_time',
        'lease_end_time': 'lease_end_time',
        'state': 'state',
        'project_id': 'project_id',
        'graph_id': 'graph_id',
        'name': 'name',
        'slice_id': 'slice_id'
    }

    def __init__(self, model=None, lease_start_time=None, lease_end_time=None, state=None, project_id=None, graph_id=None, name=None, slice_id=None):  # noqa: E501
        """Slice - a model defined in Swagger"""  # noqa: E501
        self._model = None
        self._lease_start_time = None
        self._lease_end_time = None
        self._state = None
        self._project_id = None
        self._graph_id = None
        self._name = None
        self._slice_id = None
        self.discriminator = None
        if model is not None:
            self.model = model
        if lease_start_time is not None:
            self.lease_start_time = lease_start_time
        if lease_end_time is not None:
            self.lease_end_time = lease_end_time
        if state is not None:
            self.state = state
        if project_id is not None:
            self.project_id = project_id
        self.graph_id = graph_id
        self.name = name
        self.slice_id = slice_id

    @property
    def model(self):
        """Gets the model of this Slice.  # noqa: E501


        :return: The model of this Slice.  # noqa: E501
        :rtype: str
        """
        return self._model

    @model.setter
    def model(self, model):
        """Sets the model of this Slice.


        :param model: The model of this Slice.  # noqa: E501
        :type: str
        """

        self._model = model

    @property
    def lease_start_time(self):
        """Gets the lease_start_time of this Slice.  # noqa: E501


        :return: The lease_start_time of this Slice.  # noqa: E501
        :rtype: str
        """
        return self._lease_start_time

    @lease_start_time.setter
    def lease_start_time(self, lease_start_time):
        """Sets the lease_start_time of this Slice.


        :param lease_start_time: The lease_start_time of this Slice.  # noqa: E501
        :type: str
        """

        self._lease_start_time = lease_start_time

    @property
    def lease_end_time(self):
        """Gets the lease_end_time of this Slice.  # noqa: E501


        :return: The lease_end_time of this Slice.  # noqa: E501
        :rtype: str
        """
        return self._lease_end_time

    @lease_end_time.setter
    def lease_end_time(self, lease_end_time):
        """Sets the lease_end_time of this Slice.


        :param lease_end_time: The lease_end_time of this Slice.  # noqa: E501
        :type: str
        """

        self._lease_end_time = lease_end_time

    @property
    def state(self):
        """Gets the state of this Slice.  # noqa: E501


        :return: The state of this Slice.  # noqa: E501
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """Sets the state of this Slice.


        :param state: The state of this Slice.  # noqa: E501
        :type: str
        """

        self._state = state

    @property
    def project_id(self):
        """Gets the project_id of this Slice.  # noqa: E501


        :return: The project_id of this Slice.  # noqa: E501
        :rtype: str
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        """Sets the project_id of this Slice.


        :param project_id: The project_id of this Slice.  # noqa: E501
        :type: str
        """

        self._project_id = project_id

    @property
    def graph_id(self):
        """Gets the graph_id of this Slice.  # noqa: E501


        :return: The graph_id of this Slice.  # noqa: E501
        :rtype: str
        """
        return self._graph_id

    @graph_id.setter
    def graph_id(self, graph_id):
        """Sets the graph_id of this Slice.


        :param graph_id: The graph_id of this Slice.  # noqa: E501
        :type: str
        """
        if graph_id is None:
            raise ValueError("Invalid value for `graph_id`, must not be `None`")  # noqa: E501

        self._graph_id = graph_id

    @property
    def name(self):
        """Gets the name of this Slice.  # noqa: E501


        :return: The name of this Slice.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Slice.


        :param name: The name of this Slice.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def slice_id(self):
        """Gets the slice_id of this Slice.  # noqa: E501


        :return: The slice_id of this Slice.  # noqa: E501
        :rtype: str
        """
        return self._slice_id

    @slice_id.setter
    def slice_id(self, slice_id):
        """Sets the slice_id of this Slice.


        :param slice_id: The slice_id of this Slice.  # noqa: E501
        :type: str
        """
        if slice_id is None:
            raise ValueError("Invalid value for `slice_id`, must not be `None`")  # noqa: E501

        self._slice_id = slice_id

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(Slice, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Slice):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other